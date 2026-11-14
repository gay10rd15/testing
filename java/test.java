package test;

import java.util.Scanner;
import java.util.Random;

public class test {
    public static void main(String[] args) {
        final Integer rand = new Random().nextInt(100);
        int guess = 0;
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("make a guess: ");

            try {
                guess = scanner.nextInt();

            } catch (java.util.InputMismatchException e) {

                System.err.println("you can't enter a string!");
                System.exit(1);

            }

            if (guess > rand) {
                System.out.println("Too high!");
            } else if (guess < rand) {
                System.out.println("Too low!");
            } else {
                System.out.println("Correct\nsomebody get this guy a million dollars");
                break;
            }
        }
        scanner.close();
    }
}
