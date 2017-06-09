package agh.edu.pl.sudokusolver.android.network;

import agh.edu.pl.sudokusolver.model.SudokuResult;
import io.reactivex.Observable;
import okhttp3.RequestBody;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public interface SudokuService {

    @Multipart
    @POST("upload")
    Observable<SudokuResult> postToSolve(@Part("image") RequestBody image);

}
