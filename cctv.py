import subprocess
import time
import os


def start_ffmpeg_process(rtsp_url, output_path):
    command = [
        "ffmpeg",
        "-i",
        rtsp_url,
        "-preset",
        "fast",
        "-g",
        "60",
        "-sc_threshold",
        "0",
        "-hls_time",
        "10",
        "-hls_list_size",
        "5",
        "-hls_flags",
        "delete_segments",
        "-f",
        "hls",
        output_path,
    ]
    return subprocess.Popen(command)


def main():
    # Daftar kamera CCTV
    cameras = [
        {
            "name": "Camera1",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.7:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera1/camera1_output.m3u8",
        },
        {
            "name": "Camera2",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.14:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera2/camera2_output.m3u8",
        },
        {
            "name": "Camera3",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.4:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera3/camera3_output.m3u8",
        },
        {
            "name": "Camera4",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.5:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera4/camera4_output.m3u8",
        },
        {
            "name": "Camera5",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.6:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera5/camera5_output.m3u8",
        },
        {
            "name": "Camera6",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.3:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera6/camera6_output.m3u8",
        },
        {
            "name": "Camera7",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.33:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera7/camera7_output.m3u8",
        },
        {
            "name": "Camera8",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.19:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera8/camera8_output.m3u8",
        },
        {
            "name": "Camera9",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.2:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera9/camera9_output.m3u8",
        },
        {
            "name": "Camera10",
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.21:554/Streaming/Channels/101/",
            "output_path": "C:/xampp/htdocs/cctv/video/camera10/camera10_output.m3u8",
        },
    ]

    processes = []

    try:
        for camera in cameras:
            # Pastikan direktori output ada
            os.makedirs(os.path.dirname(camera["output_path"]), exist_ok=True)

            # Mulai proses FFmpeg untuk setiap kamera
            process = start_ffmpeg_process(camera["rtsp_url"], camera["output_path"])
            processes.append(process)
            print(f"Started FFmpeg process for {camera['name']}")

        # Biarkan proses berjalan
        while True:
            time.sleep(10)  # Cek setiap 10 detik
            for i, process in enumerate(processes):
                if process.poll() is not None:
                    # Jika proses berhenti, restart
                    print(f"Restarting FFmpeg process for {cameras[i]['name']}")
                    processes[i] = start_ffmpeg_process(
                        cameras[i]["rtsp_url"], cameras[i]["output_path"]
                    )

    except KeyboardInterrupt:
        print("Stopping all processes...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()
        print("All processes stopped.")


if __name__ == "__main__":
    main()
