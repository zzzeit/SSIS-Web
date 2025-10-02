"use client";
import './colleges.css'

export default function submitCollege(codeValue, nameValue) {
    console.log("Submitting College");
    fetch(`http://127.0.0.1:5000/insert/college/${codeValue}/${nameValue}`);
}
