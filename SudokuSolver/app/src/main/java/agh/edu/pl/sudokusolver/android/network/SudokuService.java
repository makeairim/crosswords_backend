package agh.edu.pl.sudokusolver.android.network;

import agh.edu.pl.sudokusolver.model.ImageDTO;
import agh.edu.pl.sudokusolver.model.SudokuResult;
import io.reactivex.Observable;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.http.Body;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Headers;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public interface SudokuService {

    @POST("upload")
    Observable<SudokuResult> postToSolve (@Body ImageDTO file);

    @POST("upload2")
    Observable<SudokuResult> postToSolve2 (@Body RequestBody body);


}
