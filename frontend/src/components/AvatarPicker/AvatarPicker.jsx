import './AvatarPicker.css';
import { downloadFile } from '@/utils/supaClient';
import { useEffect } from 'react';

export default function AvatarPicker({ avatarUpdate = [], viewOnly = false, valueFuncs = null }) {

	useEffect(() => {
		const fetchAvatar = async () => {
			if (valueFuncs) {
				try {
					let avatarURL = await downloadFile('profile-pictures', `${valueFuncs[0][0]}`);
					avatarURL = URL.createObjectURL(avatarURL);
					avatarUpdate[3](avatarURL);
				} catch (error) {
					console.error('Error: ' + error.message);
				}
			}
		};
		fetchAvatar();
	}, [valueFuncs]);

	const openPicker = () => {
		if (viewOnly) return;
		const input = document.createElement("input");
		input.type = "file";
		input.accept = "image/jpeg";
		input.style.display = "none";
		input.addEventListener("change", () => {
			const file = input.files && input.files[0];
			if (file) {
				if (file.type !== "image/jpeg") {
					alert("Only JPEG files are allowed.");
					return;
				}
				avatarUpdate[3](URL.createObjectURL(file));
				avatarUpdate[1](file);
			}});
		document.body.appendChild(input);
		input.click();
	}

	return (
		<div>
			<div className="avatar" onClick={openPicker}>
				{avatarUpdate[2] ? (
					<img src={avatarUpdate[2]} alt="avatar" />
				) : (
					<svg width={100 * 0.5} height={100 * 0.5} viewBox="0 0 24 24" fill="none" aria-hidden>
						<circle cx="12" cy="8" r="3.2" fill="#bbb" />
						<path d="M4 20c0-3.3 3.6-6 8-6s8 2.7 8 6" fill="#bbb" />
					</svg>
				)}
			</div>
		</div>
	);
}