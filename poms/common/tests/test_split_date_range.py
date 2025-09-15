import datetime

from django.test import SimpleTestCase

from poms.common.utils import split_date_range


class TestSplitDateRange(SimpleTestCase):
    def test_basic_cases(self):
        test_cases = [
            (datetime.date(2024, 9, 17), datetime.date(2024, 10, 4), "W", False),
            (datetime.date(2024, 8, 10), datetime.date(2024, 10, 29), "M", False),
            (datetime.date(2024, 9, 2), datetime.date(2024, 9, 8), "D", True),
            (datetime.date(2024, 8, 15), datetime.date(2024, 10, 15), "M", True),
            (datetime.date(2022, 5, 15), datetime.date(2024, 5, 15), "Y", True),
            (datetime.date(2024, 1, 3), datetime.date(2024, 3, 31), "Q", False),
            (datetime.date(2024, 1, 3), datetime.date(2024, 3, 31), "Q", True),
        ]

        expected = [
            [
                ("2024-09-16", "2024-09-22"),
                ("2024-09-23", "2024-09-29"),
                ("2024-09-30", "2024-10-06"),
            ],
            [
                ("2024-08-01", "2024-08-31"),
                ("2024-09-01", "2024-09-30"),
                ("2024-10-01", "2024-10-31"),
            ],
            [
                ("2024-09-02", "2024-09-02"),
                ("2024-09-03", "2024-09-03"),
                ("2024-09-04", "2024-09-04"),
                ("2024-09-05", "2024-09-05"),
                ("2024-09-06", "2024-09-06"),
            ],
            [
                ("2024-08-01", "2024-08-30"),
                ("2024-09-02", "2024-09-30"),
                ("2024-10-01", "2024-10-31"),
            ],
            [
                ("2022-01-03", "2022-12-30"),
                ("2023-01-02", "2023-12-29"),
                ("2024-01-01", "2024-12-31"),
            ],
            [("2024-01-01", "2024-03-31")],
            [("2024-01-01", "2024-03-29")],
        ]

        for i, test_case in enumerate(test_cases):
            with self.subTest(test_case=test_case):
                dates = split_date_range(test_case[0], test_case[1], test_case[2], test_case[3])
                self.assertEqual(dates, expected[i])

    def test_invalid_frequency_raises(self):
        with self.assertRaises(ValueError):
            split_date_range(datetime.date(2024, 1, 1), datetime.date(2024, 1, 31), "Z", False)

    def test_start_after_end_raises(self):
        with self.assertRaises(ValueError):
            split_date_range(datetime.date(2024, 2, 1), datetime.date(2024, 1, 31), "M", False)

    def test_custom_frequency_returns_single_pair_and_accepts_strings(self):
        start = "2024-09-01"
        end = "2024-09-30"
        self.assertEqual(split_date_range(start, end, "C", True), [("2024-09-01", "2024-09-30")])
        self.assertEqual(split_date_range(start, end, "C", False), [("2024-09-01", "2024-09-30")])

    def test_daily_includes_weekends_when_not_bday(self):
        dates = split_date_range(datetime.date(2024, 9, 7), datetime.date(2024, 9, 9), "D", False)
        self.assertEqual(
            dates,
            [("2024-09-07", "2024-09-07"), ("2024-09-08", "2024-09-08"), ("2024-09-09", "2024-09-09")],
        )

    def test_single_day_range_business_and_weekend(self):
        # Business day
        dates = split_date_range(datetime.date(2024, 9, 4), datetime.date(2024, 9, 4), "D", True)
        self.assertEqual(dates, [("2024-09-04", "2024-09-04")])
        dates = split_date_range(datetime.date(2024, 9, 4), datetime.date(2024, 9, 4), "D", False)
        self.assertEqual(dates, [("2024-09-04", "2024-09-04")])
        # Weekend day
        dates = split_date_range(datetime.date(2024, 9, 7), datetime.date(2024, 9, 7), "D", True)
        self.assertEqual(dates, [])
        dates = split_date_range(datetime.date(2024, 9, 7), datetime.date(2024, 9, 7), "D", False)
        self.assertEqual(dates, [("2024-09-07", "2024-09-07")])

    def test_weekly_business_day_adjustments(self):
        dates = split_date_range(datetime.date(2024, 9, 17), datetime.date(2024, 10, 4), "W", True)
        self.assertEqual(
            dates,
            [("2024-09-16", "2024-09-20"), ("2024-09-23", "2024-09-27"), ("2024-09-30", "2024-10-04")],
        )
