package com.gay10rd.fancytid;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

/**
 * JavaFX App
 */
public class App extends Application {

    @Override
    public void start(Stage stage) {
        Label son = new Label("sonl");
        son.getStyleClass().add("text");
        Scene main = new Scene(son, 100, 100);
        main.getStylesheets().add(getClass().getResource("/style.css").toExternalForm());
        stage.setScene(main);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }

}