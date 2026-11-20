# Time fields

Rules for `event_date`, `pub_date` and `source_pub_datetime_utc` in
`data/events.csv`.

---

## Purpose

To put each event in the right window and keep events in their true order.

- `event_date` answers: when did the thing happen?
- `pub_date` answers: when was it reported or published?
- `source_pub_datetime_utc` answers: at exactly what time was it published,
  when that matters?

The window is assigned by `event_date`. Only when `event_date` is missing is it
assigned by `pub_date`.

---

## Required fields

Every event row must have:

- `event_date` (`YYYY-MM-DD`). Leave it blank only when it is genuinely unknown.
- `event_date_confidence` (`High`, `Med` or `Low`).
- `event_date_basis` (one of the allowed values below).
- `pub_date` (`YYYY-MM-DD`).

`source_pub_datetime_utc` is optional, but recommended when a report may fall
on different dates in UTC and in local time.

---

## Allowed values for `event_date_basis`

| Value | Use it when |
|---|---|
| `explicit_in_report` | The source states the date directly, for example "on Jan. 3". |
| `inferred_from_weekday` | The source gives only a weekday ("on Tuesday") and you work out the calendar date from `pub_date`. Use `event_date_confidence` = `Med` unless other context pins the date down. |
| `primary_doc_effective_date` | A primary document gives a date from which it applies or takes effect. Use that date as `event_date`; `pub_date` stays the date of publication or adoption. |
| `other` | None of the above applies. Explain in `notes`. |

---

## Confidence

| Level | When |
|---|---|
| `High` | The report gives an explicit calendar date, or a primary document's effective date is unambiguous. |
| `Med` | The date is inferred from a weekday and `pub_date`, or the event is said to happen "this week" with enough to anchor it. |
| `Low` | The date is unclear, inferred from vague wording, or only approximate. Explain the inference in `notes`. |

---

## Events in several steps or phases

By default, record steps that can be analysed separately as separate events.

For example:

- "Tariff announced" (the intent) and "tariff takes effect" (the enforcement):
  prefer two rows if both dates matter to the analysis.
- "Sanctions package adopted" and "sanctions enter into force": prefer two rows
  if the dates differ and the effects are likely to lag.

If you keep one row for an event in phases:

- use the `event_date` that matters most to the analysis;
- describe the phases in `notes`.

---

## Publication timestamp (`source_pub_datetime_utc`)

Use it when:

- an event happens near midnight local time and sources report in UTC;
- sources seem to disagree by one day;
- the exact order of events matters.

Format: ISO 8601 in UTC, for example `2026-01-03T23:15:00Z`. If unknown, leave
it blank.

---

## Assigning the window

- Set `window_id` to the window in `data/windows.csv` whose dates contain
  `event_date`. Both the start and end dates count as inside the window.

If `event_date` is blank:

- assign the window by `pub_date`;
- set `event_date_confidence` = `Low`;
- set `event_date_basis` = `other`;
- explain in `notes`.

When a rule compares windows as "earlier" or "later", it means by date, not by
window id. Window ids are labels and need not run in date order.
