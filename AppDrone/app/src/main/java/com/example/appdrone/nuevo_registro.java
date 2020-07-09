package com.example.appdrone;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.ActivityOptions;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.location.GpsStatus;
import android.location.Location;
import android.location.OnNmeaMessageListener;
import android.os.Build;
import android.os.Bundle;
import android.transition.Slide;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.example.appdrone.Adapters.RecyleLocationAdapter;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;

import java.util.ArrayList;
import java.util.List;

@RequiresApi(api = Build.VERSION_CODES.N)
public class nuevo_registro extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks,GoogleApiClient.OnConnectionFailedListener, GpsStatus.NmeaListener, com.google.android.gms.location.LocationListener {
    public String [] puntos_coordenados;
    public static float desplazamiento_horizontal;
    public AlertDialog ventana_progreso;
    public  ProgressBar progreso;
    private static LocationTrack locationTrack;
    List<GGA> ggaList;
    LinearLayoutManager linearLayoutManager;
    StringBuilder stringBuilderQuality=new StringBuilder();
    RecyclerView locationRecyleView;
    TextView longView;
    TextView lactView;
    TextView altView;
    TextView qualityView;

    TextView textViewLatitude;
    TextView textViewLongitude;
    TextView textViewTime;
    TextView textViewSatellites;
    TextView textViewQuality;
    RecyleLocationAdapter recyleLocationAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nuevo_registro);

        getWindow().setExitTransition(new Slide(Gravity.LEFT));
        getWindow().setEnterTransition(new Slide(Gravity.RIGHT));
        //puntos_coordenados[0]="";
        distancia distancia = new distancia();
        desplazamiento_horizontal = distancia.desplazamiento_metrico;

        ggaList=new ArrayList<>();
        locationRecyleView=findViewById(R.id.recycler_pc);
        //getSupportActionBar().hide();
        linearLayoutManager = new LinearLayoutManager(nuevo_registro.this, LinearLayoutManager.VERTICAL, false);
        linearLayoutManager.setSmoothScrollbarEnabled(true);
        recyleLocationAdapter = new RecyleLocationAdapter(this, ggaList);
        //floatingActionButton=findViewById(R.id.fabadd);
        locationRecyleView=findViewById(R.id.recycler_pc);

        locationRecyleView.setAdapter(recyleLocationAdapter);
        locationRecyleView.setLayoutManager(linearLayoutManager);

        textViewLatitude=findViewById(R.id.txtview_latitude);
        textViewLongitude=findViewById(R.id.txtview_longitude);
        textViewQuality=findViewById(R.id.txtview_quality);
        textViewSatellites=findViewById(R.id.txtview_satellitesnumber);
        textViewTime=findViewById(R.id.txtview_time);


        locationTrack=new LocationTrack.Builder().setContext(this).buildGoogleApiClient().createLocationRequest(2000,1000).addNmeaStatusListener().connectGoogleApi().build();

    }
    private void showInfo() throws Exception{

        lactView.setText(String.valueOf(locationTrack.get$GGA().getLatitude()));
        longView.setText(String.valueOf(locationTrack.get$GGA().getLongitude()));
        textViewTime.setText(locationTrack.get$GGA().getTime());
        textViewSatellites.setText(String.valueOf(locationTrack.get$GGA().getNumberOfSatellitesInUse()));

        stringBuilderQuality=new StringBuilder();
        settextViewQuality();
    }
    private void settextViewQuality() throws Exception{
        switch (locationTrack.get$GGA().getFixQuality()){

            case 0:
                stringBuilderQuality.append("invalid");
                break;
            case 1:
                stringBuilderQuality.append("GPS fix");
                break;
            case  2:
                stringBuilderQuality.append("DGPS fix");
                break;
            case 3:
                stringBuilderQuality.append("PPS fix");
                break;
            case 4:
                stringBuilderQuality.append("Real Time Kinematic");
                break;
            case 5:
                stringBuilderQuality.append("Float RTK");
                break;
            case  6:
                stringBuilderQuality.append("estimated");
                break;
            case  7:
                stringBuilderQuality.append("manual input mode");
                break;
            case  8:
                stringBuilderQuality.append("simulation mode");
                break;
            default:
        }

        textViewQuality.setText(stringBuilderQuality.toString());

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
//        barra_progreso();
//        ventana_progreso.show();
        try {
            recyleLocationAdapter.addNLocation(locationTrack.get$GGA());
        }
        catch (Exception e){
            System.out.println(("aqui fue"));
            e.printStackTrace();
        }

    }

    public void eliminar_ultima_coordenadaa(View view) {

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

    @Override
    public void onConnected(@Nullable Bundle bundle) {
        locationTrack.startLocationRequest();
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        locationTrack.connectGoogleAPI();
    }

    @Override
    public void onLocationChanged(Location location) {
        locationTrack.setCurrentLocation(location);
    }

    @Override
    public void onNmeaReceived(long timestamp, String s) {
        try {
            locationTrack.setNmeaObject(s);
            showInfo();
        }
        catch (Exception e){
            e.printStackTrace();
        }

    }



    @Override
    protected void onPause() {
        locationTrack.stopLocationRequest();
        super.onPause();
    }

    @Override
    protected void onResume() {
        locationTrack.startLocationRequest();
        super.onResume();
    }

}


