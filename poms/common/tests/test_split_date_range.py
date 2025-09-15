import datetime

from django.test import SimpleTestCase

from poms.common.utils import split_date_range


class TestSplitDateRange(SimpleTestCase):
    maxDiff = None

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

    def test_comprehensive_combinations(self):
        TEST_COMBINATIONS = [
            [
                "2024-01-01", "2024-01-05", "D", False,
                [
                    ("2024-01-01", "2024-01-01"),
                    ("2024-01-02", "2024-01-02"),
                    ("2024-01-03", "2024-01-03"),
                    ("2024-01-04", "2024-01-04"),
                    ("2024-01-05", "2024-01-05")
                ]
            ],

            # Daily with business days only (Mon-Fri, skip weekend)
            # 2024-01-01 is Monday, 2024-01-07 is Sunday
            [
                "2024-01-01", "2024-01-07", "D", True,
                [
                    ("2024-01-01", "2024-01-01"),  # Monday
                    ("2024-01-02", "2024-01-02"),  # Tuesday
                    ("2024-01-03", "2024-01-03"),  # Wednesday
                    ("2024-01-04", "2024-01-04"),  # Thursday
                    ("2024-01-05", "2024-01-05")   # Friday
                    # Weekend days (Sat, Sun) are skipped
                ]
            ],

            # Daily starting on weekend with business days only
            # 2024-01-06 is Saturday
            [
                "2024-01-06", "2024-01-09", "D", True,
                [
                    ("2024-01-08", "2024-01-08"),  # Monday (shifted from weekend)
                    ("2024-01-09", "2024-01-09")   # Tuesday
                ]
            ],

            # Week spans from Monday to Sunday
            [
                "2024-01-01", "2024-01-14", "W", False,
                [
                    ("2024-01-01", "2024-01-07"),  # Week 1: Mon-Sun
                    ("2024-01-08", "2024-01-14")   # Week 2: Mon-Sun
                ]
            ],

            # Weekly with business days only
            [
                "2024-01-01", "2024-01-14", "W", True,
                [
                    ("2024-01-01", "2024-01-05"),  # Week 1: Mon-Fri
                    ("2024-01-08", "2024-01-12")   # Week 2: Mon-Fri
                ]
            ],

            # Weekly starting mid-week
            [
                "2024-01-03", "2024-01-10", "W", False,
                [
                    ("2024-01-01", "2024-01-07"),  # Full week
                    ("2024-01-08", "2024-01-14")   # Full week
                ]
            ],

            # Full months
            [
                "2024-01-01", "2024-03-31", "M", False,
                [
                    ("2024-01-01", "2024-01-31"),  # January
                    ("2024-02-01", "2024-02-29"),  # February (2024 is leap year)
                    ("2024-03-01", "2024-03-31")   # March
                ]
            ],

            # Monthly starting mid-month
            [
                "2024-01-15", "2024-03-20", "M", False,
                [
                    ("2024-01-01", "2024-01-31"),  # Full January
                    ("2024-02-01", "2024-02-29"),  # Full February
                    ("2024-03-01", "2024-03-31")   # Full March
                ]
            ],

            # Monthly with business days only
            [
                "2024-01-01", "2024-02-29", "M", True,
                [
                    ("2024-01-01", "2024-01-31"),  # January (business days adjusted)
                    ("2024-02-01", "2024-02-29")   # February (business days adjusted)
                ]
            ],

            # Full quarters
            [
                "2024-01-01", "2024-12-31", "Q", False,
                [
                    ("2024-01-01", "2024-03-31"),  # Q1
                    ("2024-04-01", "2024-06-30"),  # Q2
                    ("2024-07-01", "2024-09-30"),  # Q3
                    ("2024-10-01", "2024-12-31")   # Q4
                ]
            ],

            # Quarterly starting mid-quarter
            [
                "2024-02-15", "2024-08-20", "Q", False,
                [
                    ("2024-01-01", "2024-03-31"),  # Full Q1
                    ("2024-04-01", "2024-06-30"),  # Full Q2
                    ("2024-07-01", "2024-09-30")   # Full Q3
                ]
            ],

            # Single quarter
            [
                "2024-01-15", "2024-02-28", "Q", False,
                [
                    ("2024-01-01", "2024-03-31")   # Full Q1
                ]
            ],

            # Multiple years
            [
                "2023-01-01", "2025-12-31", "Y", False,
                [
                    ("2023-01-01", "2023-12-31"),  # 2023
                    ("2024-01-01", "2024-12-31"),  # 2024
                    ("2025-01-01", "2025-12-31")   # 2025
                ]
            ],

            # Yearly starting mid-year
            [
                "2023-06-15", "2024-08-20", "Y", False,
                [
                    ("2023-01-01", "2023-12-31"),  # Full 2023
                    ("2024-01-01", "2024-12-31")   # Full 2024
                ]
            ],

            # Single year, partial
            [
                "2024-03-01", "2024-09-30", "Y", False,
                [
                    ("2024-01-01", "2024-12-31")   # Full 2024
                ]
            ],

            # Custom frequency (no splitting)
            [
                "2024-01-01", "2024-12-31", "C", False,
                [
                    ("2024-01-01", "2024-12-31")   # No split
                ]
            ],

            [
                "2024-01-15", "2024-01-20", "C", True,
                [
                    ("2024-01-15", "2024-01-20")   # No split, business day flag ignored
                ]
            ],

            # Same start and end date
            [
                "2024-01-01", "2024-01-01", "D", False,
                [
                    ("2024-01-01", "2024-01-01")
                ]
            ],

            # Same start and end date - weekend with business days
            [
                "2024-01-06", "2024-01-06", "D", True,
                []  # Saturday skipped when only business days
            ],

            # Very short range - 2 days
            [
                "2024-01-01", "2024-01-02", "W", False,
                [
                    ("2024-01-01", "2024-01-07")   # Full week covering the range
                ]
            ],

            # Month boundary edge case
            [
                "2024-01-31", "2024-02-01", "M", False,
                [
                    ("2024-01-01", "2024-01-31"),  # Full January
                    ("2024-02-01", "2024-02-29")   # Full February (2024 leap year)
                ]
            ],

            # Leap year February
            [
                "2024-02-01", "2024-02-29", "M", False,
                [
                    ("2024-02-01", "2024-02-29")   # Full February in leap year
                ]
            ],

            # Non-leap year February
            [
                "2023-02-01", "2023-02-28", "M", False,
                [
                    ("2023-02-01", "2023-02-28")   # Full February in non-leap year
                ]
            ],

            [
                datetime.datetime(2024, 1, 1), datetime.datetime(2024, 1, 3), "D", False,
                [
                    ("2024-01-01", "2024-01-01"),
                    ("2024-01-02", "2024-01-02"),
                    ("2024-01-03", "2024-01-03")
                ]
            ],

            [
                datetime.date(2024, 1, 1), datetime.date(2024, 1, 31), "M", False,
                [
                    ("2024-01-01", "2024-01-31")
                ]
            ],

            # Range starting and ending on weekends
            [
                "2024-01-06", "2024-01-07", "D", True,
                []  # Both Saturday and Sunday, so no business days
            ],

            # Weekly range with only weekends
            [
                "2024-01-06", "2024-01-07", "W", True,
                []  # Weekend only, no business days
            ],

            # Monthly range where first/last days need business day adjustment
            [
                "2024-01-01", "2024-01-31", "M", True,
                [
                    ("2024-01-01", "2024-01-31")  # January with business day adjustment
                ]
            ]
        ]

        for combo in TEST_COMBINATIONS:
            start, end, freq, is_bday, expected = combo
            with self.subTest(start=start, end=end, freq=freq, is_bday=is_bday):
                result = split_date_range(start, end, freq, is_bday)
                self.assertEqual(result, expected)

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
