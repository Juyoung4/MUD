import 'package:flutter/material.dart';

final kHintTextStyle = TextStyle(
  color: Colors.white54,
  fontFamily: 'OpenSans',
);

final bacgroundColors = [
  Color(0xFF73AEF5),
  Color(0xFF61A4F1),
  Color(0xFF478DE0),
  Color(0xFF398AE5),
];

final kLabelStyle = TextStyle(
  color: Colors.white,
  fontWeight: FontWeight.bold,
  fontFamily: 'OpenSans',
);

final kTitleStyle = TextStyle(
  color: Colors.white,
  fontWeight: FontWeight.bold,
  fontFamily: 'Pacifico',
  fontSize: 46,
  shadows: <Shadow>[
    Shadow(
      offset: Offset.zero,
      blurRadius: 5.0,
      color: Color(0xFF398AE5)
    ),
  ], 
);

final kTopBarTitleStyle = TextStyle(
  color: Colors.black87,
  fontWeight: FontWeight.bold,
  fontFamily: 'OpenSans',
  fontSize: 38,
  letterSpacing: 1.5
);

final kBoxDecorationStyle = BoxDecoration(
  color: Color(0xFF6CA8F1),
  borderRadius: BorderRadius.circular(10.0),
  boxShadow: [
    BoxShadow(
      color: Colors.black12,
      blurRadius: 6.0,
      offset: Offset(0, 2),
    ),
  ],
);
