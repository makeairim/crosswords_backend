package agh.edu.pl.sudokusolver.android.network;

import com.jakewharton.retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;

import java.io.File;

import agh.edu.pl.sudokusolver.model.SudokuResult;
import io.reactivex.Observable;
import okhttp3.MediaType;
import okhttp3.RequestBody;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class SudokuServiceRequestProvider {
    public static Observable<SudokuResult> solveSudoku(File file){
        MediaType MEDIA_TYPE_PNG = MediaType.parse("image/png");
        RequestBody requestBody = RequestBody.create(MEDIA_TYPE_PNG, file);
        SudokuService client = HttpClientProvider.getRetrofitBuilderInstance().addCallAdapterFactory(RxJava2CallAdapterFactory.create()).addConverterFactory(GsonConverterFactory.create()).build().create(SudokuService.class);
        return client.postToSolve(requestBody);
    }

}
