"use server";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function uploadFile(bucketName, filePath, file) {
	const { data, error } = await supabase.storage
		.from(bucketName)
		.upload(filePath, file);

	if (error) {
		console.error('Error uploading file:', error);
	} else {
		console.log('File uploaded successfully:', data);
	}
}

async function downloadFile(bucketName, filePath) {
	const { data, error } = await supabase.storage
		.from(bucketName)
		.download(filePath);

	if (error) {
		console.error('Error downloading file:', error);
	} else {
		console.log('File downloaded successfully:', data);
		return data;
	}

	return null;
}

export { uploadFile, downloadFile };