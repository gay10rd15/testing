package com.example;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
import javafx.scene.Text;



public class App extends Application {
    public void hw(Stage HS) {
        Text helptext = new Text("this is a help screen");
        Scene Hscene = new Scene(helptext, 300, 200);
        Hs.setScene(Hscene);
        HS.show();
    }

    @Override
    public void start(Stage stage) {
        // make the menu bar
        MenuBar mb = new MenuBar();

        Menu file = new Menu("File");
        Menu help = new Menu("Help");

        MenuItem helpItem = new MenuItem("help");
        MenuItem importItem = new MenuItem("import");
        
        helpItem.setOnAction(e -> hw());


        file.getItems().addAll(importItem);
        help.getItems().addAll(helpItem);
        
        mb.getMenus().addAll(file, help);

        // make Panes for the scene
        BorderPane root = new BorderPane();
        root.setTop(mb);
        Scene scene = new Scene(root, 500, 300);

        // show everything
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }

}