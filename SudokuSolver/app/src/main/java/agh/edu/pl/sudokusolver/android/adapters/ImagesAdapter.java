package agh.edu.pl.sudokusolver.android.adapters;

import android.content.Context;
import android.net.Uri;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.squareup.picasso.Picasso;

import java.util.List;

import agh.edu.pl.sudokusolver.R;

/**
 * Created by bartosz.wolcerz on 10/06/2017.
 */

public class ImagesAdapter extends RecyclerView.Adapter<ImagesAdapter.ImageAdapterViewHolder> {
        private final ImagesAdapterOnClickHandler mOnClickHandler;
        private Context mContext;
        private List<String> images;

        public ImagesAdapter(Context mContext, ImagesAdapterOnClickHandler onClickHandler) {
            this.mContext = mContext;
            this.mOnClickHandler = onClickHandler;
        }

        public void swapData(List<String> movies) {
            this.images = movies;
            notifyDataSetChanged();

        }

        public interface ImagesAdapterOnClickHandler {
            void onClick(String path);
        }

        @Override
        public ImageAdapterViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(mContext).inflate(R.layout.list_item_image, parent, false);//todo chnage layout type
            view.setFocusable(true);
            return new ImageAdapterViewHolder(view);
        }

        @Override
        public void onBindViewHolder(ImageAdapterViewHolder holder, int position) {
            String imagePath = images.get(position);
            if (imagePath != null) {
                Picasso.with(mContext).load(Uri.parse(imagePath)).into(holder.mImageIV); //fit
            }
        }

        @Override
        public long getItemId(int i) {
            return 0;
        }

        @Override
        public int getItemCount() {
            if (images == null) {
                return 0;
            }
            return images.size();
        }


        class ImageAdapterViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
            private final ImageView mImageIV;

            public ImageAdapterViewHolder(View itemView) {
                super(itemView);
                mImageIV = (ImageView) itemView.findViewById(R.id.iv_image);
                mImageIV.setOnClickListener(this);
            }

            @Override
            public void onClick(View v) {
                int pos = getAdapterPosition();
                mOnClickHandler.onClick(images.get(pos));
            }

        }
    }


