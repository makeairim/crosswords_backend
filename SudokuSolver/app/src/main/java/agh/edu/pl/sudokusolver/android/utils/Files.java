package agh.edu.pl.sudokusolver.android.utils;

import android.util.Base64;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.Calendar;
import java.util.IllegalFormatException;

import agh.edu.pl.sudokusolver.android.Preference;
import agh.edu.pl.sudokusolver.model.SudokuResult;

/**
 * Created by bartosz.wolcerz on 10/06/2017.
 */

public class Files {
    public static String generateUniqueFileName() {
        Calendar rightNow = Calendar.getInstance();
        long offset = rightNow.get(Calendar.ZONE_OFFSET) +
                rightNow.get(Calendar.DST_OFFSET);
        long sinceMidnight = (rightNow.getTimeInMillis() + offset) %
                (24 * 60 * 60 * 1000);
        return String.valueOf(sinceMidnight);
    }
    public static String getLastImagePath(){
        String baseDir = Preference.getBaseDir();
        File file=new File(baseDir);

        if(!file.isDirectory()) return null;
        File lastOne = Arrays.asList(file.listFiles()).stream().sorted((o1, o2) -> o1.getName().substring(o1.getName().lastIndexOf(File.pathSeparatorChar) + 1).compareTo(o2.getName().substring(o1.getName().lastIndexOf(File.pathSeparatorChar) + 1))).findFirst().orElse(null);
        if(lastOne!=null)
            return lastOne.getAbsolutePath();
        return null;
    }

    public static String saveSolution(SudokuResult sudokuResult) {
        String fileName=generateUniqueFileName();
        String filePath=Preference.getBaseDir();
        boolean saved = saveFile(filePath,fileName, sudokuResult.getResult());
        if(saved)return filePath+File.separator+fileName;
        return "";
    }
    private static boolean saveFile(String dir,String filename, String content){
        FileOutputStream out=null;
        File dirF=new File(dir);
        if(!dirF.exists()){
            dirF.mkdirs();
        }
        File file=null;
        boolean success=true;
        try {
             file= new File(dir+filename);
            if(file.exists()) file.delete();
            file.createNewFile();
            out=new FileOutputStream(file);
            out.getChannel().truncate(0);
            byte[] decoded = Base64.decode(content, Base64.DEFAULT);
            out.write(decoded);
        } catch (Exception  e) {
            e.printStackTrace();
            if(file!=null && out!=null){
                try {
                    out.close();
                    file.delete();
                    success=false;
                } catch (IOException e1) {
                    e1.printStackTrace();
                }

            }
        }
        finally {
            try {
                if(out!=null) {
                    out.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
                success=false;
            }
        }
        return success;
    }
}
