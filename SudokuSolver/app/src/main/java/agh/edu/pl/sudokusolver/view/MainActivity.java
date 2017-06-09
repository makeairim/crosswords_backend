package agh.edu.pl.sudokusolver.view;

import android.Manifest;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import com.karumi.dexter.Dexter;
import com.karumi.dexter.MultiplePermissionsReport;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.multi.MultiplePermissionsListener;

import java.util.List;
import java.util.concurrent.Callable;

import agh.edu.pl.sudokusolver.R;
import agh.edu.pl.sudokusolver.android.network.Utils;
import agh.edu.pl.sudokusolver.model.SudokuResult;
import agh.edu.pl.sudokusolver.presenter.MainPresenter;
import butterknife.BindView;
import butterknife.ButterKnife;
import gun0912.tedbottompicker.TedBottomPicker;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = MainActivity.class.getSimpleName();
    static final int REQUEST_IMAGE_CAPTURE = 101;
    public static final Boolean noSolutionsAvailable = true;
    private MainPresenter mainPresenter;

    @BindView(R.id.my_toolbar)
    Toolbar toolbarTop;
    @BindView(R.id.tv_test_title)
    TextView title;

    public Uri selectedImage;
    private SudokuResult solvedSudoku;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);
        setSupportActionBar(toolbarTop);
        mainPresenter = new MainPresenter();
        Dexter.withActivity(this)
                .withPermissions(Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE).withListener(new MultiplePermissionsListener() {
            @Override
            public void onPermissionsChecked(MultiplePermissionsReport report) {
                if (!report.areAllPermissionsGranted()) {
                    showFailureDialog(getString(R.string.perms_not_granted), () -> {
                        finish();
                        return true;
                    });
                }else{
                    if (noSolutionsAvailable) {
                        createBottomImagePicker();
                    }
                }
            }

            @Override
            public void onPermissionRationaleShouldBeShown(List<PermissionRequest> permissions, PermissionToken token) {

            }
        }).check();
    }

    private void createBottomImagePicker() {
        TedBottomPicker tedBottomPicker = new TedBottomPicker.Builder(MainActivity.this)
                .setOnImageSelectedListener((Uri uri) -> {
                    this.selectedImage = uri;
                    Boolean isOnline = Utils.isOnline(this).single(false).blockingGet();
                    if (!isOnline) {
                        handleNoConnection();
                    } else {
                        mainPresenter.onTakeView(this);
                    }
                })
                .create();

        tedBottomPicker.show(getSupportFragmentManager());
    }

    private void handleNoConnection() {
        showFailureDialog("No internet connection. Cannot solve sudoku", () -> true);
    }

    private void showFailureDialog(String message, Callable action) {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setTitle(getString(R.string.something_goes_wrong));
        alertDialog.setMessage(message);
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK", (dialog, which) -> {
            try {
                action.call();
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        switch (id) {
            case R.id.take_photo_item:
                createBottomImagePicker();
                break;
        }
        return super.onOptionsItemSelected(item);
    }

    public void setErrorMsg() {
        showFailureDialog("Networking error", () -> true);
    }

    public void setSolvedSudoku(SudokuResult solvedSudoku) {
        this.solvedSudoku = solvedSudoku;
    }

    public void update() {

        title.setText(solvedSudoku.getResult());
    }


//    private void takeNewPhoto() {
//        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
//        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
//            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
//        } else {
//            showFailureDialog(getString(R.string.no_camera_app), () -> {
//                return true;
//            });
//        }
// }

}
