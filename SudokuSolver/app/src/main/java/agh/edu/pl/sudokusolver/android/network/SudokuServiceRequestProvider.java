package agh.edu.pl.sudokusolver.android.network;

import android.util.Base64;

import com.jakewharton.retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;

import agh.edu.pl.sudokusolver.model.ImageDTO;
import agh.edu.pl.sudokusolver.model.SudokuResult;
import io.reactivex.Observable;
import okhttp3.MediaType;
import okhttp3.RequestBody;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class SudokuServiceRequestProvider {
    public static Observable<SudokuResult> solveSudoku(File file) {
//        MediaType MEDIA_TYPE_PNG = MediaType.parse("image/jpg");
//        RequestBody requestBody = RequestBody.create(MEDIA_TYPE_PNG,file);
//        byte[] buf;
//        InputStream in = null;
//        RequestBody requestFile = null;
//        try {
//            in = new FileInputStream(file);
//
//            buf = new byte[in.available()];
//            while (in.read(buf) != -1) ;
//            RequestBody requestBody = RequestBody
//                    .create(MediaType.parse("application/octet-stream"), buf);
//            requestFile = RequestBody.create(
//                    MediaType.parse("application/octet-stream"),
//                    buf
//            );
//        } catch (FileNotFoundException e) {
//            e.printStackTrace();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
            //RequestBody body=RequestBody.create(MediaType.parse("application/json"),(new JSONObject(new some("i","i2").toString())).toString()) ;

           // ImageDTO img = new ImageDTO("name", "content");
//        byte[] buf = new byte[0];
//        try {
//            FileInputStream in = new FileInputStream(file);
//
//            buf = new byte[in.available()];
//            while (in.read(buf) != -1) ;
//        } catch (FileNotFoundException e) {
//            e.printStackTrace();
//        } catch (IOException e) {
//            e.printStackTrace();
//
// }
        ImageDTO img=null;
        byte[] bytes = new byte[0];
        try {
            bytes=readBytes(file);
        } catch (IOException e) {
            e.printStackTrace();
        }
        img = new ImageDTO("content",new String(bytes));

        SudokuService client = HttpClientProvider.getRetrofitBuilderInstance().addCallAdapterFactory(RxJava2CallAdapterFactory.create()).build().create(SudokuService.class);
        MediaType mediaType = MediaType.parse("application/json");
        mediaType.charset(Charset.forName("UTF-8"));
        RequestBody body =
                RequestBody.create(mediaType, Base64.encodeToString(bytes,Base64.DEFAULT));
        return client.postToSolve2(body);
    }
    public static byte[] readBytes(File file) throws IOException {
        FileInputStream in = new FileInputStream(file);
        byte[] b = new byte[1024];
        ByteArrayOutputStream os = new ByteArrayOutputStream();
        int c;
        while ((c = in.read(b)) != -1) {
            os.write(b, 0, c);
        }
        return os.toByteArray();
    }
    static class some{
        String i1,i2;

        public String getI1() {
            return i1;
        }

        public void setI1(String i1) {
            this.i1 = i1;
        }

        public some(String i1, String i2) {
            this.i1 = i1;
            this.i2 = i2;
        }
    }

}
