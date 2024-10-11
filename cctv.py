import subprocess
import time
import os
import logging
import sys

# Setup logging
logging.basicConfig(
    filename="ffmpeg_process.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)


def start_ffmpeg_process(rtsp_url, output_path):
    command = [
        "ffmpeg",
        "-loglevel",
        "info",  # Gunakan 'debug' untuk lebih banyak informasi
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

    logging.info(f"Starting FFmpeg process: {' '.join(command)}")
    print(f"Starting FFmpeg process for RTSP URL: {rtsp_url}")

    try:
        # Jangan pipe stdout dan stderr untuk menghindari blocking
        return subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        logging.error(
            "FFmpeg tidak ditemukan. Pastikan FFmpeg terinstal dan ada dalam PATH."
        )
        print("FFmpeg tidak ditemukan. Pastikan FFmpeg terinstal dan ada dalam PATH.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error starting FFmpeg: {e}")
        print(f"Error starting FFmpeg: {e}")
        return None


def monitor_processes(processes, cameras):
    while True:
        time.sleep(10)  # Cek status setiap 10 detik
        for i, process in enumerate(processes):
            if process.poll() is not None:  # Jika proses berhenti
                logging.warning(
                    f"FFmpeg process for {cameras[i]['name']} stopped unexpectedly. Restarting..."
                )
                print(
                    f"FFmpeg process for {cameras[i]['name']} stopped unexpectedly. Restarting..."
                )
                processes[i] = restart_process(cameras[i])


def restart_process(camera):
    try:
        new_process = start_ffmpeg_process(camera["rtsp_url"], camera["output_path"])
        if new_process:
            logging.info(f"Successfully restarted FFmpeg process for {camera['name']}")
            print(f"Successfully restarted FFmpeg process for {camera['name']}")
        return new_process
    except Exception as e:
        logging.error(f"Failed to restart FFmpeg process for {camera['name']}: {e}")
        print(f"Failed to restart FFmpeg process for {camera['name']}: {e}")
        return None


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
            "rtsp_url": "rtsp://admin:Admin123@10.213.2.12:554/Streaming/Channels/101/",
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
            if process:
                processes.append(process)
                logging.info(f"Started FFmpeg process for {camera['name']}")
                print(f"Started FFmpeg process for {camera['name']}")
            else:
                logging.error(f"Failed to start FFmpeg process for {camera['name']}")
                print(f"Failed to start FFmpeg process for {camera['name']}")

            time.sleep(1)  # Tambahkan sedikit jeda antara tiap kamera

        if not processes:
            logging.error("Tidak ada proses FFmpeg yang berjalan. Keluar dari program.")
            print("Tidak ada proses FFmpeg yang berjalan. Keluar dari program.")
            sys.exit(1)

        # Monitor proses FFmpeg
        monitor_processes(processes, cameras)

    except KeyboardInterrupt:
        logging.info("Stopping all processes...")
        print("Stopping all processes...")
        for process in processes:
            if process:
                process.terminate()
        for process in processes:
            if process:
                process.wait()
        logging.info("All processes stopped.")
        print("All processes stopped.")


if __name__ == "__main__":
    main()
