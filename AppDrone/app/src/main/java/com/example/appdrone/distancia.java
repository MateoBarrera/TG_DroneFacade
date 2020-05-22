package com.example.appdrone;

import androidx.appcompat.app.AppCompatActivity;
import android.annotation.SuppressLint;
import android.app.ActivityOptions;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.transition.Slide;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;


public class distancia extends AppCompatActivity {
    public EditText distancia;
    public EditText angulo_h;
    public EditText angulo_v;
    public float superpocision_de_imagenes = 0.35f;
    public float distancia_metrica =0.0f;
    public float desplazamiento_metrico = 0.0f;
    public float cv_h = 90.0f;
    public float cv_v = 60.0f;

    @SuppressLint({"CutPasteId", "RtlHardcoded"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_distancia);
        getWindow().setExitTransition(new Slide(Gravity.LEFT));
        getWindow().setEnterTransition(new Slide(Gravity.TOP));
        distancia = findViewById(R.id.distancia_input);

    }
    @Override
    public boolean onKeyUp(int keyCode, KeyEvent event){
        if (keyCode == KeyEvent.KEYCODE_ENTER){

            calcular_distancia();
            return true;
        }
        return false;
    }

    public void calcular_distancia() {
          if(distancia.getText() != null && !distancia.getText().toString().equals(".") && !distancia.getText().toString().equals(",")){
              distancia_metrica = Float.parseFloat(distancia.getText().toString());
          }
    }

    public void nuevo_registro(View view) {
          if (distancia_metrica>=2.0f){
              desplazamiento_metrico = (float) (2.0f*(Math.tan(Math.toRadians(cv_h/2.0))*(1-superpocision_de_imagenes) *distancia_metrica));
              Intent intent = new Intent(this,nuevo_registro.class);
              startActivity(intent, ActivityOptions.makeSceneTransitionAnimation(this).toBundle());
         }
          else{
              AlertDialog.Builder builder = new AlertDialog.Builder(this);
              builder.setMessage(R.string.distancia_message_text).setPositiveButton(R.string.aceptar_btn, new DialogInterface.OnClickListener(){
                  public void onClick(DialogInterface dialog, int id) {

                  }
              }).setTitle(R.string.distancia_title_message);
              builder.create();
              builder.show();
          }
    }

    @SuppressLint("CutPasteId")
    public void campo_de_vision(View view) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        LayoutInflater inflater = this.getLayoutInflater();
        final View dialogView = inflater.inflate(R.layout.distancia_emergente, null);
        builder.setView(dialogView);
                builder.setMessage(R.string.distancia_emergente_text).setPositiveButton(R.string.aceptar_btn, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                angulo_h = dialogView.findViewById(R.id.input_angulo_h);
                angulo_v = dialogView.findViewById(R.id.input_angulo_v);
                onAjustarCVClick();
            }
        }).setNegativeButton(R.string.cancelar_btn, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int which) {

            }
        }).setTitle(R.string.distancia_emergente_title);

        builder.create();
        builder.show();

    }

    public void onAjustarCVClick() {

        if((!(angulo_h.getText().toString().isEmpty())) && (!(angulo_v.getText().toString().isEmpty())) && Float.parseFloat(angulo_h.getText().toString())<360 && Float.parseFloat(angulo_v.getText().toString())<360){
            cv_h = Float.parseFloat(angulo_h.getText().toString());
            cv_v = Float.parseFloat(angulo_v.getText().toString());

        }
        else{
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setMessage(R.string.angulos_incorrectos_text).setPositiveButton(R.string.aceptar_btn, new DialogInterface.OnClickListener(){
                public void onClick(DialogInterface dialog, int id) {

                }
            }).setTitle(R.string.angulos_incorrectos_title);
            builder.create();
            builder.show();
        }

    }
}