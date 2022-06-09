-- view for euro_all_info
CREATE VIEW IF NOT EXISTS euro_all_info
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
	win_results.four_one_winners,
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
