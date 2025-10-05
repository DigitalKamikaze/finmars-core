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


class TestPicDatesFromRange(SimpleTestCase):

    def test_pick_dates_from_range_custom_frequency(self):
        """Test for 'C' (custom) frequency - should return only start and end dates"""
        # Test with date objects
        result = pick_dates_from_range(
            datetime.date(2024, 1, 15),
            datetime.date(2024, 3, 20),
            "C",
            False,
            True
        )
        self.assertEqual(result, ["2024-01-15", "2024-03-20"])

        # Test with string dates
        result = pick_dates_from_range(
            "2024-01-15",
            "2024-03-20",
            "C",
            False,
            True
        )
        self.assertEqual(result, ["2024-01-15", "2024-03-20"])

        # Test with mixed types
        result = pick_dates_from_range(
            datetime.date(2024, 1, 15),
            "2024-03-20",
            "C",
            True,
            False
        )
        self.assertEqual(result, ["2024-01-15", "2024-03-20"])

    def test_pick_dates_from_range_invalid_frequency(self):
        """Test for invalid frequency - should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            pick_dates_from_range(
                datetime.date(2024, 1, 1),
                datetime.date(2024, 12, 31),
                "X",  # Invalid frequency
                False,
                True
            )
        self.assertIn("Invalid frequency", str(context.exception))

    def test_pick_dates_from_range_invalid_date_order(self):
        """Test for invalid date order - start_date > end_date"""
        with self.assertRaises(ValueError) as context:
            pick_dates_from_range(
                datetime.date(2024, 12, 31),
                datetime.date(2024, 1, 1),
                "M",
                False,
                True
            )
        self.assertIn("must be less than or equal to", str(context.exception))

    def test_pick_dates_from_range_same_date(self):
        """Test when start_date == end_date"""
        result = pick_dates_from_range(
            datetime.date(2024, 6, 15),
            datetime.date(2024, 6, 15),
            "D",
            False,
            True
        )
        # Should return the single date
        self.assertEqual(result, ["2024-06-15"])

    def test_pick_dates_from_range_weekend_handling(self):
        """Test weekend handling with is_only_bday=True"""
        # Saturday to Sunday range with daily frequency
        # 2024-09-07 is Saturday, and 2024-09-08 is Sunday
        result = pick_dates_from_range(
            datetime.date(2024, 9, 7),
            datetime.date(2024, 9, 8),
            "D",
            True,  # Only business days
            True
        )
        # Should return empty list as both are weekends
        self.assertEqual(result, [])

        # Friday to Monday with daily frequency
        result = pick_dates_from_range(
            datetime.date(2024, 9, 6),  # Friday
            datetime.date(2024, 9, 9),  # Monday
            "D",
            True,
            True
        )
        # Should return only Friday and Monday
        self.assertEqual(result, ["2024-09-06", "2024-09-09"])

    def test_pick_dates_from_range_monthly_weekend_adjustment(self):
        """Test monthly date adjustment for dates falling on weekends"""
        # If month start/end falls on a weekend, should shift to business day
        # 2024-06-01 is Saturday
        result = pick_dates_from_range(
            datetime.date(2024, 6, 1),  # Saturday
            datetime.date(2024, 8, 31),
            "M",
            True,  # Adjust to business days
            True  # Start of the month
        )
        # June 1 (Sat) should shift to June 3 (Mon)
        self.assertIn("2024-06-03", result)

    def test_pick_dates_from_range_string_input(self):
        """Test with string input data"""
        result = pick_dates_from_range(
            "2024-01-01",
            "2024-03-31",
            "M",
            False,
            True
        )
        self.assertEqual(result, ["2024-01-01", "2024-02-01", "2024-03-01"])

    def test_pick_dates_from_range_empty_result(self):
        """Test case when pd.date_range returns an empty list"""
        # Very short range that doesn't contain full period
        result = pick_dates_from_range(
            datetime.date(2024, 1, 2),
            datetime.date(2024, 1, 3),
            "Y",  # Yearly frequency
            False,
            False  # End of year
        )
        # Should return the empty list as range doesn't contain the full year
        self.assertEqual(result, [])

    def test_pick_dates_from_range_no_duplicates(self):
        """Test that the result contains no duplicate dates"""
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "Q",
            False,
            True
        )
        # Check no duplicates
        self.assertEqual(len(result), len(set(result)))

    def test_pick_dates_from_range_quarterly_business_days(self):
        """Test quarterly frequency with business day adjustment"""
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "Q",
            True,  # Only business days
            True  # Start of quarter
        )
        # All dates should be business days
        for date_str in result:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            self.assertTrue(date_obj.weekday() < 5, f"{date_str} is not a business day")

    def test_pick_dates_from_range_half_yearly_start(self):
        """Test half-yearly frequency - start of half-year periods"""
        # Full year - both halves
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            True  # Start of half-year
        )
        self.assertEqual(result, ["2024-01-01", "2024-07-01"])

        # Multiple years
        result = pick_dates_from_range(
            datetime.date(2023, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2023-01-01", "2023-07-01", "2024-01-01", "2024-07-01"])

        # Starting mid-first half
        result = pick_dates_from_range(
            datetime.date(2024, 3, 15),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-03-15", "2024-07-01"])

        # Starting mid-second half
        result = pick_dates_from_range(
            datetime.date(2024, 9, 15),
            datetime.date(2025, 6, 30),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-09-15", "2025-01-01"])

        # Only first half
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 6, 30),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-01-01"])

        # Only second half
        result = pick_dates_from_range(
            datetime.date(2024, 7, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-07-01"])

    def test_pick_dates_from_range_half_yearly_end(self):
        """Test half-yearly frequency - end of half-year periods"""
        # Full year - both halves
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            False  # End of half-year
        )
        self.assertEqual(result, ["2024-06-30", "2024-12-31"])

        # Multiple years
        result = pick_dates_from_range(
            datetime.date(2023, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            False
        )
        self.assertEqual(result, ["2023-06-30", "2023-12-31", "2024-06-30", "2024-12-31"])

        # Partial first half
        result = pick_dates_from_range(
            datetime.date(2024, 2, 15),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            False
        )
        self.assertEqual(result, ["2024-06-30", "2024-12-31"])

        # Partial second half
        result = pick_dates_from_range(
            datetime.date(2024, 8, 15),
            datetime.date(2025, 3, 31),
            "HY",
            False,
            False
        )
        self.assertEqual(result, ["2024-12-31", "2025-03-31"])

        # Crossing half-year boundary
        result = pick_dates_from_range(
            datetime.date(2024, 5, 1),
            datetime.date(2024, 8, 31),
            "HY",
            False,
            False
        )
        self.assertEqual(result, ["2024-06-30", "2024-08-31"])

    def test_pick_dates_from_range_half_yearly_with_business_days(self):
        """Test half-yearly frequency with business day adjustments"""
        # Full year with business days - start of half-year
        # 2024-01-01 is Monday, 2024-07-01 is Monday
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            True,  # Only business days
            True  # Start of half-year
        )
        self.assertEqual(result, ["2024-01-01", "2024-07-01"])

        # Full year with business days - end of half-year
        # 2024-06-30 is Sunday, should shift to 2024-06-28 (Friday)
        # 2024-12-31 is Tuesday
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            True,
            False  # End of half-year
        )
        self.assertEqual(result, ["2024-06-28", "2024-12-31"])

        # Starting on weekend - 2024-06-01 is Saturday
        result = pick_dates_from_range(
            datetime.date(2024, 6, 1),  # Saturday
            datetime.date(2024, 12, 31),
            "HY",
            True,
            True
        )
        # Should include adjusted start date and July 1
        self.assertIn("2024-06-03", result)  # Monday
        self.assertIn("2024-07-01", result)

        # Multiple years with business day adjustment
        result = pick_dates_from_range(
            datetime.date(2023, 1, 1),  # Sunday
            datetime.date(2024, 12, 31),
            "HY",
            True,
            True
        )
        # 2023-01-01 is Sunday, should shift to 2023-01-02 (Monday)
        self.assertIn("2023-01-02", result)
        self.assertIn("2023-07-03", result)  # 2023-07-01 is Saturday, shifts to Monday
        self.assertIn("2024-01-01", result)  # Monday
        self.assertIn("2024-07-01", result)  # Monday

    def test_pick_dates_from_range_half_yearly_string_input(self):
        """Test half-yearly frequency with string date inputs"""
        result = pick_dates_from_range(
            "2024-01-01",
            "2024-12-31",
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-01-01", "2024-07-01"])

        result = pick_dates_from_range(
            "2024-01-01",
            "2024-12-31",
            "HY",
            False,
            False
        )
        self.assertEqual(result, ["2024-06-30", "2024-12-31"])

    def test_pick_dates_from_range_half_yearly_leap_year(self):
        """Test half-yearly frequency with leap year"""
        # 2024 is a leap year
        result = pick_dates_from_range(
            datetime.date(2024, 2, 29),  # Leap day
            datetime.date(2024, 12, 31),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-02-29", "2024-07-01"])

        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            False
        )
        # June 30 should be included (leap year doesn't affect this)
        self.assertEqual(result, ["2024-06-30", "2024-12-31"])

    def test_pick_dates_from_range_half_yearly_edge_cases(self):
        """Test half-yearly frequency edge cases"""
        # Exactly one half-year period
        result = pick_dates_from_range(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 6, 30),
            "HY",
            False,
            True
        )
        self.assertEqual(result, ["2024-01-01"])

        # Very short range within one half
        result = pick_dates_from_range(
            datetime.date(2024, 2, 1),
            datetime.date(2024, 2, 28),
            "HY",
            False,
            False
        )
        # Should return empty list as no complete half-year period exists in this range
        self.assertEqual(result, [])

        # Three years span
        result = pick_dates_from_range(
            datetime.date(2022, 1, 1),
            datetime.date(2024, 12, 31),
            "HY",
            False,
            True
        )
        self.assertEqual(result, [
            "2022-01-01", "2022-07-01",
            "2023-01-01", "2023-07-01",
            "2024-01-01", "2024-07-01"
        ])


class TestCalcPeriodDate(SimpleTestCase):
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
        """Edge cases, weekends with business day adjustment"""
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
