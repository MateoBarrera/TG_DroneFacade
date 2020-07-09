package com.example.appdrone;


import android.annotation.SuppressLint;
import android.location.GpsStatus;
import android.location.Location;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.appdrone.Adapters.RecyleLocationAdapter;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;

import java.util.ArrayList;
import java.util.List;

public class locationMain extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks,GoogleApiClient.OnConnectionFailedListener, GpsStatus.NmeaListener, com.google.android.gms.location.LocationListener {

    private static LocationTrack locationTrack;
    RecyclerView locationRecyleView;
    Button floatingActionButton;
    RecyleLocationAdapter recyleLocationAdapter;
    List<GGA> ggaList;
    LinearLayoutManager linearLayoutManager;
    StringBuilder stringBuilderQuality=new StringBuilder();

    TextView textViewLatitude;
    TextView textViewLongitude;
    TextView textViewTime;
    TextView textViewSatellites;
    TextView textViewQuality;

    @RequiresApi(api = Build.VERSION_CODES.N)
    @SuppressLint("WrongViewCast")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_location);


        ggaList=new ArrayList<>();
        linearLayoutManager=new LinearLayoutManager(locationMain.this, LinearLayoutManager.VERTICAL,false);
        linearLayoutManager.setSmoothScrollbarEnabled(true);
        recyleLocationAdapter=new RecyleLocationAdapter(this, ggaList);
        floatingActionButton=findViewById(R.id.badd);
        locationRecyleView=findViewById(R.id.recylerview_location);

        locationRecyleView.setAdapter(recyleLocationAdapter);
        locationRecyleView.setLayoutManager(linearLayoutManager);

        textViewLatitude=findViewById(R.id.txtview_latitude);
        textViewLongitude=findViewById(R.id.txtview_longitude);
        textViewQuality=findViewById(R.id.txtview_quality);
        textViewSatellites=findViewById(R.id.txtview_satellitesnumber);
        textViewTime=findViewById(R.id.txtview_time);


        locationTrack=new LocationTrack.Builder().setContext(this).buildGoogleApiClient().createLocationRequest(2000,1000).addNmeaStatusListener().connectGoogleApi().build();
        System.out.println(("stared"));
        floatingActionButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    recyleLocationAdapter.addNLocation(locationTrack.get$GGA());
                }
                catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
    }

    @Override
    public void onNmeaReceived(long l, String s) {
        try {
            System.out.println((s));
            locationTrack.setNmeaObject(s);
            showInfo();
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }

    private void showInfo() throws Exception{

        textViewLatitude.setText(String.valueOf(locationTrack.get$GGA().getLatitude()));
        textViewLongitude.setText(String.valueOf(locationTrack.get$GGA().getLongitude()));
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

    @Override
    public void onConnected(Bundle bundle) {
        locationTrack.startLocationRequest();
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        locationTrack.connectGoogleAPI();

    }

    @Override
    public void onLocationChanged(Location location) {
        locationTrack.setCurrentLocation(location);
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
