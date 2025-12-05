
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function uploadFile(bucketName, filePath, file) {
	const { data, error } = await supabase.storage
		.from(bucketName)
		.upload(filePath, file, { upsert: true });

	if (error) {
		console.error('Error uploading file:', error);
        return null;
	} else {
		console.log('File uploaded successfully:', data);
        return data;
	}
}

async function downloadFile(bucketName, filePath) {
	const { data, error } = await supabase.storage
		.from(bucketName)
		.download(filePath);

	if (error) {
		console.error('Error downloading file:', error);
        return null;
	} else {
		console.log('File downloaded successfully:', data);
		return data;
	}

	return null;
}

async function renameFile(bucketName, oldFileName, newFileName) {
    try {
        // Step 1: Download the old file
        const { data: fileData, error: downloadError } = await supabase.storage
            .from(bucketName)
            .download(oldFileName);

        if (downloadError) {
            throw new Error(`Error downloading file: ${downloadError.message}`);
        }

        // Step 2: Upload the file with the new name
        const { error: uploadError } = await supabase.storage
            .from(bucketName)
            .upload(newFileName, fileData);

        if (uploadError) {
            throw new Error(`Error uploading file with new name: ${uploadError.message}`);
        }

        // Step 3: Delete the old file
        const { error: deleteError } = await supabase.storage
            .from(bucketName)
            .remove([oldFileName]);

        if (deleteError) {
            throw new Error(`Error deleting old file: ${deleteError.message}`);
        }

        console.log(`File renamed from ${oldFileName} to ${newFileName}`);
    } catch (error) {
        console.error('Error renaming file:', error.message);
    }
}

async function updateFile(bucketName, oldFileName, newFileName, newFile) {
	try {
		await renameFile(bucketName, oldFileName, newFileName);
		if (newFile) {
			await uploadFile(bucketName, newFileName, newFile);
		}
        return true;
	} catch (error) {
		console.error('Error updating file:', error.message);
        return null;
	}
}

export { uploadFile, downloadFile, renameFile, updateFile };