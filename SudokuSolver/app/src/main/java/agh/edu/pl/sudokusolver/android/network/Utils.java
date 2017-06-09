package agh.edu.pl.sudokusolver.android.network;

import android.content.Context;
import android.net.ConnectivityManager;

import io.reactivex.Observable;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class Utils {
        static public Observable<Boolean> isOnline(Context context) {
            return Observable.defer(() -> Observable.just(isOnlineCheck(context)));
        }
        static private boolean isOnlineCheck(Context context) {
            ConnectivityManager cm =
                    (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
            return cm.getActiveNetworkInfo() != null &&
                    cm.getActiveNetworkInfo().isConnectedOrConnecting();
        }
}
