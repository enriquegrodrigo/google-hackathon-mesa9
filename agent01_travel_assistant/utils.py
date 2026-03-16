import datetime
import re


def clean_html(raw_html):
    """
    A simple function to remove HTML tags.
    For more robust HTML stripping, consider using a library like BeautifulSoup.
    """
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def format_directions_to_markdown(directions_result):
    markdown_output = []

    if not directions_result:
        return "No directions found."

    for i, route in enumerate(directions_result):
        markdown_output.append(f"## Route {i+1}")
        if "warnings" in route and route["warnings"]:
            markdown_output.append(f"**Warnings:** {' '.join(route['warnings'])}")
        if "summary" in route and route["summary"]:
            markdown_output.append(f"**Summary:** {route['summary']}")
        markdown_output.append("")

        for leg_index, leg in enumerate(route["legs"]):
            markdown_output.append(
                f"### Leg {leg_index + 1}: {leg.get('start_address', '')} to {leg.get('end_address', '')}"
            )
            markdown_output.append(
                f"**Overall Leg Duration:** {leg['duration']['text']}, **Overall Leg Distance:** {leg['distance']['text']}"
            )
            markdown_output.append("")

            for step_index, step in enumerate(leg["steps"]):
                instruction_text = clean_html(step.get("html_instructions", ""))

                line = f"{step_index + 1}. **{step.get('travel_mode', 'Step')}:** {instruction_text}"
                line += f" ({step['duration']['text']}, {step['distance']['text']})"
                markdown_output.append(line)

                if "transit_details" in step:
                    transit = step["transit_details"]
                    line_details = []
                    if "line" in transit:
                        line_name = transit["line"].get("short_name") or transit[
                            "line"
                        ].get("name", "N/A")
                        vehicle_type = (
                            transit["line"].get("vehicle", {}).get("name", "")
                        )
                        headsign = transit.get("headsign", "")
                        line_details.append(
                            f"  - **Line:** {line_name} ({vehicle_type}) towards {headsign}"
                        )

                    departure_stop = transit.get("departure_stop", {}).get(
                        "name", "N/A"
                    )
                    departure_time = transit.get("departure_time", {}).get(
                        "text", "N/A"
                    )
                    line_details.append(
                        f"  - **Departure:** {departure_stop} at {departure_time}"
                    )

                    arrival_stop = transit.get("arrival_stop", {}).get("name", "N/A")
                    arrival_time = transit.get("arrival_time", {}).get("text", "N/A")
                    line_details.append(
                        f"  - **Arrival:** {arrival_stop} at {arrival_time}"
                    )

                    num_stops = transit.get("num_stops", "N/A")
                    line_details.append(f"  - **Stops:** {num_stops}")
                    markdown_output.extend(line_details)

                if "steps" in step:
                    for sub_step_index, sub_step in enumerate(step["steps"]):
                        sub_instruction_text = clean_html(
                            sub_step.get("html_instructions", "")
                        )
                        markdown_output.append(
                            f"  - {sub_instruction_text} ({sub_step['duration']['text']}, {sub_step['distance']['text']})"
                        )

            markdown_output.append("")
        markdown_output.append("---")

    return "\n".join(markdown_output)


def _consolidate_daily_hours(daily_hours):
    """Groups days with identical hours."""
    if not daily_hours:
        return []

    consolidated = []
    processed_days = set()
    day_indices = list(range(1, 7)) + [0]

    for i in day_indices:
        if i in processed_days:
            continue

        current_day_name = _get_day_name(i)
        current_hours = tuple(sorted(daily_hours.get(i, ["Closed"])))

        group = [current_day_name]
        processed_days.add(i)

        for j in range(day_indices.index(i) + 1, len(day_indices)):
            next_day_index = day_indices[j]
            next_day_hours = tuple(sorted(daily_hours.get(next_day_index, ["Closed"])))
            if next_day_hours == current_hours:
                group.append(_get_day_name(next_day_index))
                processed_days.add(next_day_index)
            else:
                break

        if len(group) > 2:
            day_range = f"{group[0]} - {group[-1]}"
        elif len(group) == 2:
            day_range = f"{group[0]}, {group[1]}"
        else:
            day_range = group[0]

        hours_str = ", ".join(current_hours)
        consolidated.append(f"{day_range}: {hours_str}")

    return consolidated


def _format_time(hour, minute):
    """Formats hour and minute (0-23, 0-59) into HH:MM AM/PM."""
    if hour is None or minute is None:
        return "N/A"
    time_obj = datetime.time(hour, minute)
    return time_obj.strftime("%I:%M %p").lstrip("0")


def _format_period(period_obj):
    """Formats a single period object into 'OpenTime - CloseTime'."""
    open_info = period_obj.get("open", {})
    close_info = period_obj.get("close", {})

    open_day = open_info.get("day")
    open_hour = open_info.get("hour")
    open_minute = open_info.get("minute")

    if open_day == 0 and open_hour == 0 and open_minute == 0 and not close_info:
        return "Open 24 hours"

    close_day = close_info.get("day")
    close_hour = close_info.get("hour")
    close_minute = close_info.get("minute")

    if open_hour == 0 and open_minute == 0 and close_hour == 0 and close_minute == 0:
        pass

    open_time_str = _format_time(open_hour, open_minute)

    if not close_info or close_hour is None or close_minute is None:
        return f"Open from {open_time_str}"

    close_time_str = _format_time(close_hour, close_minute)

    if open_day is not None and close_day is not None and open_day != close_day:
        return f"{open_time_str} - {close_time_str} (next day)"
    else:
        return f"{open_time_str} - {close_time_str}"


def format_opening_hours(opening_hours_data, current_dt=None):
    """
    Converts Google Places API opening hours object to a human-readable string.

    Args:
        opening_hours_data (dict): The opening hours object from the API.
        current_dt (datetime.datetime, optional): The current datetime, ideally
                                                 timezone-aware for accurate special day checks.
                                                 If None, special day checks for "today" are skipped.

    Returns:
        str: A human-readable representation of the opening hours.
    """
    if not opening_hours_data:
        return "Opening hours not available."

    output_lines = []

    secondary_type = opening_hours_data.get("secondaryHoursType")
    if secondary_type:
        type_str = secondary_type.replace("_", " ").title()
        output_lines.append(f"--- {type_str} Hours ---")

    open_now = opening_hours_data.get("openNow")
    if open_now is not None:
        status = "Open now" if open_now else "Closed now"
        output_lines.append(status)

    special_days_output = []
    today_is_special = False
    if current_dt and "specialDays" in opening_hours_data:
        today_date_obj = current_dt.date()
        for special_day in opening_hours_data.get("specialDays", []):
            s_date_info = special_day.get("date")
            if not s_date_info:
                continue

            s_year = s_date_info.get("year", 0)
            s_month = s_date_info.get("month")
            s_day = s_date_info.get("day")

            if not s_month or not s_day:
                continue

            special_date_matches_today = False
            if s_year == 0:
                if today_date_obj.month == s_month and today_date_obj.day == s_day:
                    special_date_matches_today = True
                    date_str = f"{today_date_obj.strftime('%B %d')} ({today_date_obj.year}, Special Hours)"
                else:
                    date_str = f"Special Hours on {datetime.date(2000, s_month, s_day).strftime('%B %d')}"
            else:
                try:
                    special_date = datetime.date(s_year, s_month, s_day)
                    date_str = f"{special_date.strftime('%Y-%m-%d')} (Special Hours)"
                    if special_date == today_date_obj:
                        special_date_matches_today = True
                except ValueError:
                    date_str = f"Invalid Special Date ({s_year}-{s_month}-{s_day})"

            day_schedule = ""
            if special_day.get("isClosed"):
                day_schedule = "Closed"
            elif special_day.get("openAllDay"):
                day_schedule = "Open 24 hours"
            elif "periods" in special_day:
                periods = special_day.get("periods", [])
                if periods:
                    day_schedule = ", ".join([_format_period(p) for p in periods])
                else:
                    day_schedule = "Closed"
            else:
                day_schedule = "Special hours (check details)"

            if special_date_matches_today:
                output_lines.append(f"TODAY ({date_str}): {day_schedule}")
                today_is_special = True
            else:
                pass

    if "weekdayDescriptions" in opening_hours_data and not today_is_special:
        output_lines.extend(opening_hours_data["weekdayDescriptions"])
    elif "periods" in opening_hours_data:
        daily_hours = {i: [] for i in range(7)}
        is_always_open = False

        periods = opening_hours_data.get("periods", [])

        if len(periods) == 1:
            p = periods[0]
            if (
                p.get("open", {}).get("day") == 0
                and p.get("open", {}).get("hour") == 0
                and p.get("open", {}).get("minute") == 0
                and not p.get("close")
            ):
                is_always_open = True

        if is_always_open:
            output_lines.append("Open 24 hours, 7 days a week")
        else:
            sorted_periods = sorted(
                periods,
                key=lambda p: (
                    p.get("open", {}).get("day", 7),
                    p.get("open", {}).get("hour", 24),
                    p.get("open", {}).get("minute", 60),
                ),
            )

            for period in sorted_periods:
                open_day = period.get("open", {}).get("day")
                if open_day is not None:
                    formatted = _format_period(period)
                    open_info = period.get("open", {})
                    close_info = period.get("close", {})
                    if (
                        open_info.get("hour") == 0
                        and open_info.get("minute") == 0
                        and close_info.get("hour") == 0
                        and close_info.get("minute") == 0
                        and close_info.get("day") == (open_info.get("day") + 1) % 7
                    ):
                        formatted = "Open 24 hours"

                    daily_hours[open_day].append(formatted)

            for day_index in range(7):
                if not daily_hours[day_index]:
                    is_covered = False
                    for p in sorted_periods:
                        close_day = p.get("close", {}).get("day")
                        open_day_p = p.get("open", {}).get("day")
                        if close_day == day_index and close_day != open_day_p:
                            is_covered = True
                            break
                    if not is_covered:
                        daily_hours[day_index] = ["Closed"]
                else:
                    if (
                        len(daily_hours[day_index]) == 1
                        and daily_hours[day_index][0] == "Open 24 hours"
                    ):
                        daily_hours[day_index] = ["Open 24 hours"]
                    daily_hours[day_index] = sorted(list(set(daily_hours[day_index])))

            consolidated_lines = _consolidate_daily_hours(daily_hours)
            output_lines.extend(consolidated_lines)

    if special_days_output:
        output_lines.append("\n--- Upcoming Special Hours ---")
        output_lines.extend(special_days_output)

    if len(output_lines) == 0 or (
        len(output_lines) == 1 and output_lines[0].startswith("---")
    ):
        return "Opening hours data incomplete or unavailable."

    return "\n".join(output_lines)
