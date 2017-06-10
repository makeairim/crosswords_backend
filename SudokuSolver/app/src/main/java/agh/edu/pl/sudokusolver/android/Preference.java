package agh.edu.pl.sudokusolver.android;

import android.net.Uri;
import android.os.Environment;
import android.util.Base64;

import java.io.File;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class Preference {
    private static final String BASE_URL = "http://10.0.2.2:8080/";
    private static final String BASE_DIR = "SudokuSolver/solutions/";

    public static String getBaseUrl() {
        return BASE_URL;
    }

    public static String getBaseDir() {
//        Environment.getExternalStorageDirectory()+BASE_DIR;
        return Environment.getExternalStorageDirectory().getAbsolutePath() + File.separator+ BASE_DIR;
    }

}
