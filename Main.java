import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        DatabaseManager dbManager = new DatabaseManager();
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to Online Quiz Application!");
        System.out.println("1. Login");
        System.out.println("2. Register");
        System.out.print("Choose an option: ");
        int choice = scanner.nextInt();
        scanner.nextLine(); // consume newline

        String username = "";
        boolean loggedIn = false;

        if (choice == 1) {
            System.out.print("Username: ");
            username = scanner.nextLine();
            System.out.print("Password: ");
            String password = scanner.nextLine();
            loggedIn = dbManager.authenticateUser(username, password);
            if (!loggedIn) {
                System.out.println("Invalid credentials.");
                dbManager.close();
                scanner.close();
                return;
            }
        } else if (choice == 2) {
            System.out.print("Username: ");
            username = scanner.nextLine();
            System.out.print("Password: ");
            String password = scanner.nextLine();
            if (dbManager.registerUser(username, password)) {
                System.out.println("Registration successful. Please login.");
                dbManager.close();
                scanner.close();
                return;
            } else {
                System.out.println("Registration failed.");
                dbManager.close();
                scanner.close();
                return;
            }
        } else {
            System.out.println("Invalid choice.");
            dbManager.close();
            scanner.close();
            return;
        }

        if (loggedIn) {
            System.out.println("Login successful. Starting quiz...");
            List<Question> questions = dbManager.getQuestions();
            Quiz quiz = new Quiz(questions, 60); // 60 seconds timer
            quiz.startQuiz();

            int userId = dbManager.getUserId(username);
            dbManager.saveResult(userId, quiz.getScore(), quiz.getTotalQuestions(), 60); // assuming time taken is 60 for simplicity
            System.out.println("Results saved.");
        }

        dbManager.close();
        scanner.close();
    }
}
