package Tools;


import java.util.Scanner;

public class Tools {
    public static void print(String string) {
        System.out.println(string);
    }
    public static void main(String[] args) {
        print("bois");
    }
    public static String input(String prompt) {
        print(prompt);
        try (Scanner ui = new Scanner(System.in)) {
            return ui.nextLine();
        }
    }
}