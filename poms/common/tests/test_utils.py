import datetime

from django.test import SimpleTestCase

from poms.common.utils import (
    calculate_period_date,
    get_last_business_day_in_previous_quarter,
    get_last_business_day_of_previous_month,
    get_last_business_day_of_previous_year,
    get_list_of_dates_between_two_dates,
    pick_dates_from_range,
)


class TestBusinessDayFunctions(SimpleTestCase):
    def test_last_business_day_of_previous_year(self):
        test_cases = [
            (datetime.date(2022, 4, 15), datetime.date(2021, 12, 31)),
            (datetime.date(2024, 7, 30), datetime.date(2023, 12, 29)),
            (datetime.date(2023, 12, 31), datetime.date(2022, 12, 30)),
        ]
        for date, expected_day in test_cases:
            with self.subTest(date=date):
                last_business_day = get_last_business_day_of_previous_year(date)
                self.assertEqual(last_business_day, expected_day)

    def test_last_business_day_of_previous_month(self):
        test_cases = [
            (datetime.date(2023, 6, 15), datetime.date(2023, 5, 31)),
            (datetime.date(2023, 10, 1), datetime.date(2023, 9, 29)),
            (datetime.date(2024, 1, 2), datetime.date(2023, 12, 29)),
        ]
        for date, expected_day in test_cases:
            with self.subTest(date=date):
                last_business_day = get_last_business_day_of_previous_month(date)
                self.assertEqual(last_business_day, expected_day)

    def test_last_business_day_in_previous_quarter(self):
        test_cases = [
            (datetime.date(2023, 4, 15), datetime.date(2023, 3, 31)),
            (datetime.date(2023, 11, 1), datetime.date(2023, 9, 29)),
            (datetime.date(2024, 7, 2), datetime.date(2024, 6, 28)),
        ]
        for date, expected_day in test_cases:
            with self.subTest(date=date):
                last_business_day = get_last_business_day_in_previous_quarter(date)
                self.assertEqual(last_business_day, expected_day)

    def test_pick_dates_from_range(self):
        test_cases = [
            (datetime.date(2024, 8, 3), datetime.date(2024, 10, 13), "M", True, True),
            (datetime.date(2024, 8, 3), datetime.date(2024, 10, 13), "M", False, False),
            (datetime.date(2024, 8, 31), datetime.date(2024, 10, 1), "W", True, True),
            (datetime.date(2024, 8, 31), datetime.date(2024, 10, 1), "W", False, True),
            (datetime.date(2022, 12, 15), datetime.date(2024, 12, 3), "Y", False, True),
            (
                datetime.date(2022, 12, 15),
                datetime.date(2024, 12, 14),
                "Y",
                True,
                False,
            ),
            (datetime.date(2024, 9, 1), datetime.date(2024, 9, 5), "D", True, False),
            (datetime.date(2024, 1, 1), datetime.date(2024, 5, 1), "Q", False, True),
            (datetime.date(2023, 12, 15), datetime.date(2024, 4, 1), "Q", False, True),
            (datetime.date(2023, 12, 15), datetime.date(2024, 4, 1), "Q", False, False),
        ]

        expected = [
            ["2024-08-05", "2024-09-02", "2024-10-01"],
            ["2024-08-31", "2024-09-30", "2024-10-13"],
            ["2024-09-02", "2024-09-09", "2024-09-16", "2024-09-23"],
            ["2024-08-31", "2024-09-02", "2024-09-09", "2024-09-16", "2024-09-23"],
            ["2022-12-15", "2023-01-01", "2024-01-01"],
            ["2022-12-30", "2023-12-29", "2024-12-13"],
            ["2024-09-02", "2024-09-03", "2024-09-04", "2024-09-05"],
            ["2024-01-01", "2024-04-01"],
            ["2023-12-15", "2024-01-01", "2024-04-01"],
            ["2023-12-31", "2024-03-31", "2024-04-01"],
        ]

        for i, test_case in enumerate(test_cases):
            dates = pick_dates_from_range(test_case[0], test_case[1], test_case[2], test_case[3], test_case[4])
            self.assertEqual(dates, expected[i])

    def test_get_calc_period_date(self):
        test_cases = [
            (datetime.date(2024, 12, 1), "M", -3, False, False),
            (datetime.date(2024, 12, 1), "M", 3, True, True),
            (datetime.date(2024, 9, 1), "W", 2, False, True),
            (datetime.date(2024, 9, 1), "W", 2, True, False),
            (datetime.date(2024, 12, 1), "Y", -1, False, False),
            (datetime.date(2024, 9, 4), "D", 3, True, True),
            (datetime.date(2024, 1, 1), "Q", 1, False, True),
            (datetime.date(2024, 1, 1), "Q", 2, False, False),
        ]

        expected = [
            "2024-09-30",
            "2025-03-03",
            "2024-09-09",
            "2024-09-13",
            "2023-12-31",
            "2024-09-09",
            "2024-04-01",
            "2024-06-30",
        ]

        for i, test_case in enumerate(test_cases):
            date = calculate_period_date(test_case[0], test_case[1], test_case[2], test_case[3], test_case[4])
            self.assertEqual(date, expected[i])

    def test_get_calc_period_date_shift_zero(self):
        """Tests for (shift=0) should return start/end of the period"""
        test_cases = [
            # Month
            (datetime.date(2024, 9, 15), "M", 0, False, True),
            (datetime.date(2024, 9, 15), "M", 0, False, False),
            # Quarter
            (datetime.date(2024, 2, 15), "Q", 0, False, True),
            (datetime.date(2024, 2, 15), "Q", 0, False, False),
            # Year
            (datetime.date(2024, 6, 15), "Y", 0, False, True),
            (datetime.date(2024, 6, 15), "Y", 0, False, False),
            # Week
            (datetime.date(2024, 9, 4), "W", 0, False, True),
            (datetime.date(2024, 9, 4), "W", 0, False, False),
            # Days
            (datetime.date(2024, 9, 15), "D", 0, False, True),
            (datetime.date(2024, 9, 15), "D", 0, False, False),
        ]

        expected = [
            "2024-09-01",
            "2024-09-30",
            "2024-01-01",
            "2024-03-31",
            "2024-01-01",
            "2024-12-31",
            "2024-09-02",
            "2024-09-08",
            "2024-09-15",
            "2024-09-15",
        ]

        for i, test_case in enumerate(test_cases):
            with self.subTest(case=i, input=test_case):
                date = calculate_period_date(test_case[0], test_case[1], test_case[2], test_case[3], test_case[4])
                self.assertEqual(date, expected[i],
                    f"Test case {i}: {test_case} expected {expected[i]}, got {date}")

    def test_get_calc_period_date_edge_cases(self):
        """Edge cases, weekends с business day adjustment"""
        string_result = calculate_period_date("2024-09-15", "M", 1, False, True)
        self.assertEqual(string_result, "2024-10-01")

        custom_result = calculate_period_date(datetime.date(2024, 9, 15), "C", 5, True, True)
        self.assertEqual(custom_result, "2024-09-15")

        weekend_result = calculate_period_date(datetime.date(2024, 9, 7), "D", 0, True, True)
        self.assertEqual(weekend_result, "2024-09-09")  # Monday

        # Saturday 2024-09-07 end of day with business day should move to Friday
        weekend_end_result = calculate_period_date(datetime.date(2024, 9, 7), "D", 0, True, False)
        self.assertEqual(weekend_end_result, "2024-09-06")  # Friday


class TestListDates(SimpleTestCase):
    def test_same_day(self):
        today = datetime.date.today()
        self.assertEqual(len(get_list_of_dates_between_two_dates(today, today)), 1)

    def test_two_days(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        self.assertEqual(len(get_list_of_dates_between_two_dates(today, tomorrow)), 2)
