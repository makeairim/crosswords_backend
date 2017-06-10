package agh.edu.pl.sudokusolver.presenter;

import android.net.Uri;
import android.util.Log;

import java.io.File;
import java.util.concurrent.TimeUnit;

import agh.edu.pl.sudokusolver.android.network.SudokuServiceRequestProvider;
import agh.edu.pl.sudokusolver.android.utils.Files;
import agh.edu.pl.sudokusolver.model.SudokuResult;
import agh.edu.pl.sudokusolver.view.MainActivity;
import io.reactivex.Observable;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class MainPresenter {
    private MainActivity view;
    private Disposable sudokuSolvedDisposable;
    private String msg;
    private boolean error;
    private String sudokuResultPath;
    public static final String TAG = MainPresenter.class.getSimpleName();
    private Object selectedPhotoSolution;
    private String lastPhoto;

    public void onTakeView(MainActivity view) {
        this.view = view;
        error = false;
        sudokuSolvedDisposable = null; //todo cancel request
        if (view.selectedImage != null) {
            getSelectedPhotoSolution();
        }
        getLatestSolution();
    }

    private void getLatestSolution() {
        String path = Files.getLastImagePath();
        if (path == null) return;
        File file = new File(path);
        if (selectedPhotoSolution != null) {
            if (!file.getAbsolutePath().equals(selectedPhotoSolution)) {
                publish();
            }
        }
    }

    File getFile(Uri uri) {
        File file = new File(uri.getPath());
        return file;
    }

    void setError(String msg) {
        error = true;
        this.msg = msg;
    }

    private Observable<SudokuResult> retrieveSolvedSudoku(File file) {
        Observable<SudokuResult> result = SudokuServiceRequestProvider.solveSudoku(file).timeout(5000, TimeUnit.SECONDS);
        return result.subscribeOn(Schedulers.newThread()).observeOn(AndroidSchedulers.mainThread());
    }

    private void publish() {
        if (error) {
            view.setErrorMsg(msg);
        } else if (sudokuResultPath != null) {
            view.setSolvedSudoku(sudokuResultPath);
            view.update();
        }
        if (!sudokuSolvedDisposable.isDisposed()) sudokuSolvedDisposable.dispose();
        sudokuSolvedDisposable = null;
    }


    public void getSelectedPhotoSolution() {
        File file = getFile(view.selectedImage);
        if (file.exists()) {
            sudokuSolvedDisposable = retrieveSolvedSudoku(file).
                    doOnError(throwable -> {
                        setError("Error from server");
                        Log.d(TAG, "onTakeView: ");
                        throwable.printStackTrace();
                    }).
                    doFinally(() -> publish()).
                    subscribe(sudokuResult -> {
                        error = sudokuResult.getResult() != null ? false : true;
                        if (!error) {
                            //this.sudokuResultPath = Files.saveSolution(sudokuResult);
                            //if (this.sudokuResultPath == null || sudokuResultPath.isEmpty()) {
                            //setError(sudokuResult.getResult());
                            this.sudokuResultPath=sudokuResult.getResult();
                            publish();
                                //setError("Incorrect file format from server");
                            //}
                        }
                    });


        } else {
            setError("File does not exist");
            publish();
        }
    }
}