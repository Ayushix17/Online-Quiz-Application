import java.util.List;
import java.util.Scanner;
import java.util.Timer;
import java.util.TimerTask;

public class Quiz {
    private List<Question> questions;
    private int score;
    private int timeLimit; // in seconds
    private Timer timer;
    private boolean timeUp;
    private Scanner scanner;

    public Quiz(List<Question> questions, int timeLimit) {
        this.questions = questions;
        this.score = 0;
        this.timeLimit = timeLimit;
        this.timeUp = false;
        this.scanner = new Scanner(System.in);
    }

    public void startQuiz() {
        System.out.println("Quiz started! You have " + timeLimit + " seconds.");
        timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                timeUp = true;
                System.out.println("\nTime's up!");
            }
        }, timeLimit * 1000);

        long startTime = System.currentTimeMillis();

        for (Question q : questions) {
            if (timeUp) break;
            System.out.println("\n" + q.getQuestionText());
            System.out.println("A. " + q.getOptionA());
            System.out.println("B. " + q.getOptionB());
            System.out.println("C. " + q.getOptionC());
            System.out.println("D. " + q.getOptionD());
            System.out.print("Your answer: ");
            String answer = scanner.nextLine().toUpperCase();
            if (q.isCorrect(answer)) {
                score++;
            }
        }

        long endTime = System.currentTimeMillis();
        int timeTaken = (int) ((endTime - startTime) / 1000);
        timer.cancel();

        System.out.println("\nQuiz finished!");
        System.out.println("Score: " + score + "/" + questions.size());
        System.out.println("Time taken: " + timeTaken + " seconds");
    }

    public int getScore() {
        return score;
    }

    public int getTotalQuestions() {
        return questions.size();
    }
}
