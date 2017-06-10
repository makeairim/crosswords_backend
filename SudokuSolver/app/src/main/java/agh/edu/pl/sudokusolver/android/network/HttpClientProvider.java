package agh.edu.pl.sudokusolver.android.network;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.jakewharton.retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;

import agh.edu.pl.sudokusolver.android.Preference;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class HttpClientProvider {
    static private OkHttpClient client;
    static private Retrofit.Builder retrofitBuilder;

    static OkHttpClient getOkHttpInstance() {
        if (client == null) {
            client = new OkHttpClient.Builder().
                    addInterceptor(chain -> {
                        Request request = chain.request();
                        HttpUrl url = request.url().newBuilder().build();
                        request = request.newBuilder().url(url).build();
                        return chain.proceed(request);
                    }).build();
        }
        return client;
    }

    public static Retrofit.Builder getRetrofitBuilderInstance() {
        if (retrofitBuilder == null) {
            Gson gson = new GsonBuilder()
                    .setLenient()
                    .create();
            RxJava2CallAdapterFactory rxJava2CallAdapterFactory=RxJava2CallAdapterFactory.create();
            retrofitBuilder = new Retrofit.Builder().addConverterFactory(GsonConverterFactory.create(gson)).addCallAdapterFactory(rxJava2CallAdapterFactory)
                    .baseUrl(Preference.getBaseUrl());
        }
        return retrofitBuilder;
    }

}