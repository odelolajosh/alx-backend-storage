-- Creates a stored procedure ComputeAverageScoreForUser
-- ComputeAverageScoreForUser computes and store the average score
-- for a student.

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE average INT DEFAULT 0;
	
	SELECT AVG(score) INTO average
	FROM corrections AS c
	WHERE c.user_id = user_id;

	UPDATE users SET average_score = average
	WHERE users.id = user_id;
END //
DELIMITER ;

