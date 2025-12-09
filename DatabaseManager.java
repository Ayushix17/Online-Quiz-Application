import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class DatabaseManager {
    private static final String URL = "jdbc:mysql://localhost:3306/online_quiz";
    private static final String USER = "root"; // Change if needed
    private static final String PASSWORD = ""; // Change if needed

    private Connection connection;

    public DatabaseManager() {
        try {
            connection = DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public boolean authenticateUser(String username, String password) {
        String query = "SELECT * FROM users WHERE username = ? AND password = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, username);
            stmt.setString(2, password);
            ResultSet rs = stmt.executeQuery();
            return rs.next();
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean registerUser(String username, String password) {
        String query = "INSERT INTO users (username, password) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, username);
            stmt.setString(2, password);
            stmt.executeUpdate();
            return true;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public List<Question> getQuestions() {
        List<Question> questions = new ArrayList<>();
        String query = "SELECT * FROM questions";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            while (rs.next()) {
                Question q = new Question(
                    rs.getInt("id"),
                    rs.getString("question_text"),
                    rs.getString("option_a"),
                    rs.getString("option_b"),
                    rs.getString("option_c"),
                    rs.getString("option_d"),
                    rs.getString("correct_answer")
                );
                questions.add(q);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return questions;
    }

    public void saveResult(int userId, int score, int totalQuestions, int timeTaken) {
        String query = "INSERT INTO quiz_results (user_id, score, total_questions, time_taken_seconds) VALUES (?, ?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, userId);
            stmt.setInt(2, score);
            stmt.setInt(3, totalQuestions);
            stmt.setInt(4, timeTaken);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public int getUserId(String username) {
        String query = "SELECT id FROM users WHERE username = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, username);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return rs.getInt("id");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return -1;
    }

    public void close() {
        try {
            if (connection != null) {
                connection.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
