package com.example.appdrone;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Handler;


import android.os.Bundle;

public class splash extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent intent = new Intent(splash.this, MainActivity.class);
                startActivity(intent);
                finish();
            }
        },2000);
    }

    public static class locationMain {
    }
}
