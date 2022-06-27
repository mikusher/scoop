-- view for euro_all_info
CREATE OR replace  VIEW euro_all_info
AS
SELECT
	euro_game_day.id,
	euro_game_day.game_date,
	euro_all.million,
	euro_all.ball_week_1,
	euro_all.ball_week_2,
	euro_all.ball_week_3,
	euro_all.ball_week_4,
	euro_all.ball_week_5,
	euro_all.star_week_1,
	euro_all.star_week_2,
	win_results.five_two_winners,
	win_results.five_two_money,
	win_results.five_one_winners,
	win_results.five_one_money,
	win_results.five_winners,
	win_results.five_money,
	win_results.four_two_winners,
	win_results.four_two_money,
	win_results.four_one_winners,
	win_results.four_one_money,
	win_results.four_winners,
	win_results.four_money,
	win_results.three_two_winners,
	win_results.three_two_money,
	win_results.three_one_winners,
	win_results.three_one_money,
	win_results.three_winners,
	win_results.three_money,
	win_results.two_two_winners,
	win_results.two_two_money,
	win_results.two_one_winners,
	win_results.two_one_money,
	win_results.one_two_winners,
	win_results.one_two_money
FROM
	euro_game_day
INNER JOIN euro_all ON euro_all.game_date_id = euro_game_day.id
INNER JOIN win_results ON win_results.game_date_id = euro_game_day.id;


CREATE OR replace  VIEW concat_all
AS
SELECT
    game_date,
    CONCAT(ball_week_1, ' ', ball_week_2, ' ', ball_week_3, ' ', ball_week_4, ' ', ball_week_5) AS "Numbers",
    CONCAT(star_week_1, ' ', star_week_2) AS "Stars"
FROM euro_all_info
ORDER BY game_date DESC;

-- Note: Unless you save your query, these tabs will NOT persist if you clear your cookies or change browsers.

CREATE OR replace  VIEW view_all_content
AS
SELECT
    euro_game_day.game_date,
    euro_all.ball_week_1 as "num_one",
    euro_all.ball_week_2 as "num_two",
    euro_all.ball_week_3 as "num_tre",
    euro_all.ball_week_4 as "num_fou",
    euro_all.ball_week_5 as "num_fiv",
    euro_all.star_week_1 as "str_one",
    euro_all.star_week_2 as "str_two",
    euro_star_numbers.euro_numbers as "collect_numbers",
    euro_star_numbers.star_numbers as "collect_stars",
    euro_all.million
FROM euro_star_numbers
    INNER JOIN euro_all ON euro_all.game_date_id = euro_star_numbers.game_date_id
    INNER JOIN euro_game_day ON euro_game_day.id = euro_star_numbers.game_date_id
ORDER BY euro_game_day.game_date DESC;


CREATE OR replace  VIEW view_union_number_star
AS
SELECT
    euro_game_day.game_date,
    unums.numbers as "numbers",
    union_star.stars as "stars"
FROM union_number unums
    INNER JOIN euro_game_day ON euro_game_day.id = unums.game_date_id
    INNER JOIN union_star ON euro_game_day.id = union_star.game_date_id
ORDER BY euro_game_day.game_date DESC;