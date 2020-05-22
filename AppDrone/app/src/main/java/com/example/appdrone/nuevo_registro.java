package com.example.appdrone;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

import android.app.ActivityOptions;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.transition.Slide;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ProgressBar;

public class nuevo_registro extends AppCompatActivity {
    public String [] puntos_coordenados;
    public static float desplazamiento_horizontal;
    public AlertDialog ventana_progreso;
    public  ProgressBar progreso;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nuevo_registro);

        getWindow().setExitTransition(new Slide(Gravity.LEFT));
        getWindow().setEnterTransition(new Slide(Gravity.RIGHT));
        //puntos_coordenados[0]="";
        distancia distancia = new distancia();
        desplazamiento_horizontal = distancia.desplazamiento_metrico;

    }

    public void guardar_puntos(View view) {
        //puntos_coordenados[0].isEmpty()
        if (1 < 0) {
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setMessage(R.string.save_no_message_text).setPositiveButton(R.string.save_no_positivo, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // FIRE ZE MISSILES!
                }
            }).setNegativeButton(R.string.save_no_negativo, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int which) {
                    onDialogNegativeClick();

                }
            }).setTitle(R.string.save_no_title_message);
            builder.create();
            builder.show();
        }
        else{
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setMessage(R.string.save_ok_message_text).setPositiveButton(R.string.save_ok_positivo, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    onDialogPositiveClick();
                }
            }).setTitle(R.string.save_ok_title_message);
            builder.create();
            builder.show();

        }

    }

    public void onDialogPositiveClick() {
        Intent intent = new Intent(this,MainActivity.class);
        startActivity(intent, ActivityOptions.makeSceneTransitionAnimation(this).toBundle());

    }

    public void onDialogNegativeClick() {
        Intent intent = new Intent(this,MainActivity.class);
        startActivity(intent, ActivityOptions.makeSceneTransitionAnimation(this).toBundle());

    }

    public void capturar_coordenadas(View view) throws InterruptedException {
        barra_progreso();

    }

    public void eliminar_ultima_coordenadaa(View view) {
        ventana_progreso.show();
    }

    public void barra_progreso(){
        AlertDialog.Builder builder_capturar = new AlertDialog.Builder(this);
        LayoutInflater inflater = this.getLayoutInflater();
        final View dialogView = inflater.inflate(R.layout.capturar_coordenadas, null);
        builder_capturar.setView(dialogView);
        progreso = dialogView.findViewById(R.id.progressBar);



        builder_capturar.setMessage(R.string.capturar_text).setTitle(R.string.capturar_title).setPositiveButton(R.string.aceptar_btn, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
            }
        });

        ventana_progreso = builder_capturar.create();

    }

}


