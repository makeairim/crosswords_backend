package agh.edu.pl.sudokusolver.android.network;

import agh.edu.pl.sudokusolver.android.Preference;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import retrofit2.Retrofit;

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
            retrofitBuilder = new Retrofit.Builder().
                    client(getOkHttpInstance()).baseUrl(Preference.getBaseUrl());
        }
        return retrofitBuilder;
    }

}