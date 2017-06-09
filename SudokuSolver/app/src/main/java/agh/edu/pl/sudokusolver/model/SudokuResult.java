package agh.edu.pl.sudokusolver.model;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

import android.os.Parcel;
import android.os.Parcelable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SudokuResult implements Parcelable {

    @SerializedName("path")
    @Expose
    private String path;
    @SerializedName("result")
    @Expose
    private String result;
    public final static Parcelable.Creator<SudokuResult> CREATOR = new Creator<SudokuResult>() {


        @SuppressWarnings({
                "unchecked"
        })
        public SudokuResult createFromParcel(Parcel in) {
            SudokuResult instance = new SudokuResult();
            instance.path = ((String) in.readValue((String.class.getClassLoader())));
            instance.result = ((String) in.readValue((String.class.getClassLoader())));
            return instance;
        }

        public SudokuResult[] newArray(int size) {
            return (new SudokuResult[size]);
        }

    };

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeValue(path);
        dest.writeValue(result);
    }

    public int describeContents() {
        return 0;
    }

}