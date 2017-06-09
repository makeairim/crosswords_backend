package agh.edu.pl.sudokusolver.presenter;

import android.net.Uri;
import android.util.Log;

import java.io.File;
import java.util.concurrent.TimeUnit;

import agh.edu.pl.sudokusolver.android.network.SudokuServiceRequestProvider;
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
    private SudokuResult sudokuResult;
public static final String TAG=MainPresenter.class.getSimpleName();
    public void onTakeView(MainActivity view) {
        this.view = view;
        error = false;
        sudokuSolvedDisposable = null; //todo cancel request
        File file = getFile(view.selectedImage);
        if (file.exists()) {
            sudokuSolvedDisposable = retrieveSolvedSudoku(file).
                    doOnError(throwable -> {setError("Error from server");
            Log.d(TAG, "onTakeView: "+throwable.getMessage());}).
                    doFinally(() -> publish()).
                    subscribe(sudokuResult ->
                    this.sudokuResult = sudokuResult);
        } else {
            setError("File does not exist");
            publish();
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
            view.setErrorMsg();
            return;
        }

        view.setSolvedSudoku(sudokuResult);
        view.update();
    }


}
