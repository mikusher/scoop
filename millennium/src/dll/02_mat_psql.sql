DROP MATERIALIZED VIEW IF EXISTS materialize_all_content;
CREATE MATERIALIZED VIEW materialize_all_content
AS
    SELECT
        euro_game_day.id,
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
    ORDER BY euro_game_day.game_date DESC
    WITH NO DATA;

REFRESH MATERIALIZED VIEW materialize_all_content;


DROP MATERIALIZED VIEW IF EXISTS materialize_euro_all_info;
CREATE MATERIALIZED VIEW materialize_euro_all_info
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
    FROM euro_game_day
        INNER JOIN euro_all ON euro_all.game_date_id = euro_game_day.id
        INNER JOIN win_results ON win_results.game_date_id = euro_game_day.id
    ORDER BY euro_game_day.game_date DESC
    WITH NO DATA;
