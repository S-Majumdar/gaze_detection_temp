import React, {useState} from 'react'
import Webcam from "react-webcam";
import ReactPlayer from 'react-player/lazy'
//importing ui components
import Header from '../components/Header'
import { Button, Modal } from "@material-ui/core/"
import { makeStyles } from '@material-ui/core/styles';
import '../LessThan4YearsPage/LessThan4YearsPage'


const useStyles = makeStyles((theme) => ({
  paper: {
      position: 'absolute',
      width: 400,
      backgroundColor: theme.palette.background.paper,
      border: '2px solid #000',
      boxShadow: theme.shadows[5],
      padding: theme.spacing(2, 4, 3),
  },
}));

function MoreThan4YearsPage() {

  const webcamRef = React.useRef(null);
  const mediaRecorderRef = React.useRef(null);
  const [capturing, setCapturing] = React.useState(false);
  const [recordedChunks, setRecordedChunks] = React.useState([]);

  const [open, setOpen] = useState(false);
  const classes = useStyles()

  const handleStartCaptureClick = React.useCallback(() => {
    console.log("started capturing")
    setCapturing(true);
    mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
      mimeType: "video/webm"
    });
    mediaRecorderRef.current.addEventListener(
      "dataavailable",
      handleDataAvailable
    );
    mediaRecorderRef.current.start();
  }, [webcamRef, setCapturing, mediaRecorderRef]);

  const handleDataAvailable = React.useCallback(
    ({ data }) => {
      if (data.size > 0) {
        setRecordedChunks((prev) => prev.concat(data));
      }
    },
    [setRecordedChunks]
  );

  const handleStopCaptureClick = React.useCallback(() => {
    console.log("stopped capturing")
    mediaRecorderRef.current.stop();
    setCapturing(false);
  }, [mediaRecorderRef, webcamRef, setCapturing]);

  const handleDownload = React.useCallback(() => {
    console.log("downloading")
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, {
        type: "video/webm"
      });
      console.log(recordedChunks)
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      a.href = url;
      a.download = "react-webcam-stream-capture.webm";
      console.log(a.className)
      a.click();
      console.log(url)
      window.URL.revokeObjectURL(url);
      setRecordedChunks([]);
      setOpen(true);
    }
  }, [recordedChunks]);

  return (
    <div>
      <Header />
      {
        //Modal Component
      }
      {/* <>
      <Modal style={{display:'flex',alignItems:'center',justifyContent:'center'}} open={open} onClose={e => setOpen(false)}>
                <div className={classes.paper}>
                    <h1>This is a model</h1>
                    <h1>WOWOWOW ANOTHER MODAL</h1>
                </div>
            </Modal>
      </> */}
      {
        //Video Component
      }
      <div style={{ paddingTop: "20px", display: "flex", justifyContent: "center", alignItems: "center" }}>
        <ReactPlayer
          style={{ minWidth: "140vh", minHeight: "79vh" }}
          playing
          url='https://www.youtube.com/watch?v=rUWxSEwctFU&ab_channel=IanRushton'
          onStart={handleStartCaptureClick}
          onEnded={handleStopCaptureClick}
        />
      </div>
      {
        //Webcam Component
      }
      <div className="webcam__download__container">
        <Webcam
          style={{borderRadius:"30px"}}
          audio={false}
          ref={webcamRef}
          width={150}
          height={150}
        />

        {/* {capturing ? (
        <button onClick={handleStopCaptureClick}>Stop Capture</button>
      ) : (
          <button onClick={handleStartCaptureClick}>Start Capture</button>
        )}
      */}
        {recordedChunks.length > 0 && (
          <Button className="less__than__3__download__button" style={{borderRadius:"30px", fontSize:"20px"}} color="primary" variant="contained" onClick={handleDownload}>Download</Button>
        )}
      </div>
    </div>
  );

}

export default MoreThan4YearsPage;
