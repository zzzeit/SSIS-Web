"use client";
import './colleges.css'

export default function submitCollege(codeValue, nameValue) {
    console.log("Submitting College");
    fetch(`http://192.168.1.50:5000/insert/college/${codeValue}/${nameValue}`);
}
