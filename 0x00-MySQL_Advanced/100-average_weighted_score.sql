-- creates a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
	DECLARE weight_avg FLOAT DEFAULT 0;
	
	SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
	INTO weight_avg FROM corrections
	JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;
	
	UPDATE users SET users.average_score = IFNULL(weight_avg, 0)
	WHERE users.id = user_id;
END //
DELIMITER ;

