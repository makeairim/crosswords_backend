package agh.edu.pl.sudokusolver.model;

import com.google.gson.annotations.SerializedName;

/**
 * Created by bartosz.wolcerz on 09/06/2017.
 */

public class ImageDTO {
    @SerializedName("name")
    String name;
    @SerializedName("content")
    String content;

    public ImageDTO(String name, String content) {
        this.name = name;
        this.content = content;
    }
}
