package com.example.appdrone;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.ActivityOptions;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.transition.Slide;
import android.view.Gravity;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {
    public EditText entrada_mision;
    public String nombre_mision="";

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        getWindow().setExitTransition(new Slide(Gravity.TOP));
        getWindow().setEnterTransition(new Slide(Gravity.RIGHT));
        entrada_mision = findViewById(R.id.mision_input);

    }

    public void new_mission(View view){
        nombre_mision = entrada_mision.getText().toString();
        if(!nombre_mision.isEmpty() ){
            nombre_mision = entrada_mision.getText().toString();
            Intent intent = new Intent(this,info_1.class);
            startActivity(intent, ActivityOptions.makeSceneTransitionAnimation(this).toBundle());
            entrada_mision.setText("");

        }
        else{
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setMessage(R.string.mision_message_text).setPositiveButton(R.string.aceptar_btn, new DialogInterface.OnClickListener(){
                public void onClick(DialogInterface dialog, int id) {
                    // FIRE ZE MISSILES!
                }
            }).setTitle(R.string.mision_title_message);
            builder.create();
            builder.show();
        }


    }
}
