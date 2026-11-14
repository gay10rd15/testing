package com.gay10rd.ted;

import jexer.TApplication;
import jexer.TExceptionDialog;
import jexer.TInputBox;
import jexer.TKeypress;
import jexer.TMessageBox;
import jexer.event.TMenuEvent;
import jexer.menu.TMenu;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

import java.util.Properties;

public class App extends TApplication {
    public static Properties prop = new Properties();
    public static File configFile = new File(System.getProperty("user.home"), ".config/ted/config.conf");

    public App() throws Exception {
        super(BackendType.XTERM);

        TMenu tools = addMenu("\u2261");
        TMenu file = addMenu("&File");

        tools.addItem(TMenu.MID_QUIT, "Quit", TKeypress.kbQ);
        file.addItem(2001, "Import", TKeypress.kbI);

        try {
            FileInputStream fis = new FileInputStream(configFile);
            prop.load(fis);

        } catch (FileNotFoundException __) {
            if (configFile.getParentFile() != null) {
                configFile.getParentFile().mkdirs();
            }
            configFile.createNewFile();
        }
        if (!prop.containsKey("downloadP")) {

            prop.setProperty("downloadP", Path.of(System.getProperty("user.home"), "/Downloads").toString());
            prop.store(new FileWriter(configFile), " Config file for ted");
        }
    }

    @Override
    protected boolean onMenu(TMenuEvent event) {
        if (event.getId() == 2001) {
            try {
                download();
            } catch (IOException e) {

                e.printStackTrace();
                TExceptionDialog d = new TExceptionDialog(this, e);
                d.show();
            }
            return true;
        }
        return super.onMenu(event);
    }

    public static void main(String[] args) throws Exception {
        App app = new App();
        app.run();
    }

    public void download() throws IOException {
        TInputBox window = inputBox("URL", "Enter URL:", "", TMessageBox.Type.OKCANCEL);
        String url;
        if (window.getResult() == TMessageBox.Result.OK) {
            url = window.getText();
        } else {
            return;
        }

        String os = System.getProperty("os.name").toLowerCase();
        String binaryName;
        if (os.contains("win")) {
            binaryName = "yt-dlp.exe";
        } else if (os.contains("mac")) {
            binaryName = "yt-dlp_macos";
        } else {
            binaryName = "yt-dlp_linux";
        }

        Path tempFile = Path.of(System.getProperty("java.io.tmpdir"), binaryName);
        if (!Files.exists(tempFile)) {
            try (InputStream in = App.class.getResourceAsStream("/bin/" + binaryName)) {
                if (in == null) {
                    throw new RuntimeException("Bundled binary not found: " + binaryName);
                }
                Files.copy(in, tempFile, StandardCopyOption.REPLACE_EXISTING);
            }
        }

        File executable = tempFile.toFile();
        executable.setExecutable(true);

        String outputTemplate = Path.of(prop.getProperty("downloadP"), "video").toString();
        ProcessBuilder pb = new ProcessBuilder(
                executable.getAbsolutePath(),
                "-o", outputTemplate,
                url.trim());
        pb.redirectOutput(ProcessBuilder.Redirect.DISCARD);
        File errorLog = new File(System.getProperty("java.io.tmpdir"), "ytdlp_error.log");
        pb.redirectError(errorLog);

        Process process = pb.start();
        new Thread(() -> {
            try {
                int exitCode = process.waitFor();
                invokeLater(() -> {
                    if (exitCode == 0) {
                        messageBox("Success", "Download complete!");
                    } else {
                        messageBox("Error", "Download failed with exit code: " + exitCode);
                    }
                });
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
    }
}