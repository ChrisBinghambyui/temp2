"""
Step 1 By Hand: 5 minutes
Step 2 Approach: 5 minutes
Step 3 Pseudocode: 60 minutes
Step 4 Copilot: like 2 minutes
Step 5 Compare and Contrast: 13 minutes
Step 6 Update: 15 minutes
Step 7 Trace: 27 minutes
Step 8 Efficiency: 12 minutes



By hand, compute the number of days between the following dates:

15th of October, 1999 and 25th of October, 1999.
- 10 days
23rd of October, 1999 and 1st of December, 1999.
- 39 days
21st of October, 1999 and the 4th of March, 2004.
- 69 + (365 *4) +64 = 1593 days


==========Approach:
 use the leap year formula we made, then count. I'll assign each whole month a value of days, and have it add one to february if it's a leap year. then I'll count the number of days since jan 1 1970, then subtract the second one from the first, leaving me with the number of days

 

==========my pseudocode:

    leap_years = []
    FOR year FROM 1970 TO 2100:
        IF (year % 4 == 0 AND year % 100 != 0) OR (year % 400 == 0):
            APPEND year TO leap_years

    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    GET date1
    GET date2

    date1_years = 0
    date1_leaps = 0
    FOR year FROM 1970 TO (date1.year - 1):
        date1_years += 1
        IF year IN leap_years:
            date1_leaps += 1

    date2_years = 0
    date2_leaps = 0
    FOR year FROM 1970 TO (date2.year - 1):
        date2_years += 1
        IF year IN leap_years:
            date2_leaps += 1

    date1_month_days = 0
    FOR month_index FROM 0 TO (date1.month - 2):
        date1_month_days += months[month_index]
    IF date1.month > 2 AND date1.year IN leap_years:
        date1_month_days += 1

    date2_month_days = 0
    FOR month_index FROM 0 TO (date2.month - 2):
        date2_month_days += months[month_index]
    IF date2.month > 2 AND date2.year IN leap_years:
        date2_month_days += 1

    total_days1 = (date1_years * 365) + date1_leaps + date1_month_days + date1.day
    total_days2 = (date2_years * 365) + date2_leaps + date2_month_days + date2.day

    difference = total_days1 - total_days2
    IF difference < 0:
        difference = difference * -1

    RETURN difference



==========AI pseudocode
// Helper function to determine if a year is a leap year
FUNCTION is_leap_year(year):
    IF (year % 4 == 0 AND year % 100 != 0) OR (year % 400 == 0):
        RETURN True
    ELSE:
        RETURN False

// Main function to convert a date to total days since Jan 1, 1970
FUNCTION calculate_days_since_epoch(day, month, year):
    SET total_days = 0
    SET months_distribution = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    // 1. Count days for all full years since 1970
    FOR y FROM 1970 TO (year - 1):
        IF is_leap_year(y):
            total_days += 366
        ELSE:
            total_days += 365

    // 2. Count days for all full months in the current year
    FOR m FROM 1 TO (month - 1):
        total_days += months_distribution[m - 1]
        
    // Add the extra leap day if we are past February in a leap year
    IF month > 2 AND is_leap_year(year):
        total_days += 1

    // 3. Add the days of the current month
    total_days += day

    RETURN total_days

// FINAL CALCULATION
INPUT date1 (d1, m1, y1)
INPUT date2 (d2, m2, y2)

SET days1 = calculate_days_since_epoch(d1, m1, y1)
SET days2 = calculate_days_since_epoch(d2, m2, y2)

SET difference = ABS(days1 - days2)
PRINT "The total difference in days is: " + difference



==========Compare and contrast:
Provide an analysis as to the pros and cons of the two solutions?
    the ai one definetly seems more streamlined and polished. I think they'd both work, and I'm more comfortable reading mine.
How can your solution be improved based on what Copilot provided?
    I've got some chunkiness that could be refined. I wanted something that made sense to me first, but that also led to a bit too much slowness and probably inefficient.
How can Copilot's solution be improved based on what you know?
    It doesn't have as much legibility to me. the comments help, but it would be really hard for me to go back in and tinker with stuff
Does the pseudocode in Step 3 and Step 4 match the algorithm you performed in Step 1?
    yup



==========Trace
"""