import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useState } from 'react';
import { Button, CircularProgress, Collapse, FilledInput, FormControl, IconButton, InputAdornment, InputLabel } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { CommentCard } from './comment-card';
import { styled } from '@mui/material/styles';
import axios from 'axios';
import { getUserData } from '../../lib/auth';

const ExpandMore = styled((props) => {
    const { expand, onClick, ...other } = props;
    return <Button variant="text" startIcon={<IconButton  {...other} />} onClick={onClick}>
        {expand ? "Sembunyikan Komentar" : "Lihat Komentar"}
    </Button>;
})(({ theme, expand }) => ({
    transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
    }),
}));

export const InfoCard = ({ info, ...rest }) => {

    const [expanded, setExpanded] = useState(false);
    const [comments, setComments] = useState([]);
    const [inputComment, setInputComment] = useState("");
    const [loading, setLoading] = useState(false);
    const [sendLoading, setSendLoading] = useState(false);
    const handleExpandClick = () => {
        setExpanded(!expanded)
        if (!expanded) {
            setLoading(true)
            fetchData()
        }
    };

    const randomColor = () => {
        let hex = Math.floor(Math.random() * 0xFFFFFF);
        let color = "#" + hex.toString(16);

        return color;
    }

    const fetchData = () => {
        axios
            .get(`https://desa.agasyan.my.id/api/komentar-pengumuman/all/${info.id}`)
            .then((response) => {
                const { data } = response;
                let formatedData = data.map((e) => ({color: randomColor(), ...e}));
                console.log(formatedData)
                setLoading(false);
                if (response.status === 200) {
                    //check the api call is success by stats code 200,201 ...etc
                    setComments(formatedData.sort((a, b) => (a.created_at_utc < b.created_at_utc) ? 1 : -1));
                } else {
                    //error handle section
                }
            })
            .catch((error) => {console.log(error);setLoading(false);});
    };


    const handleSendIcon = () => {
        if (!sendLoading) {
            console.log({
                title: "",
                isi: inputComment,
                pengumuman_id: info.id,
                user_id: getUserData().id
            })
            setSendLoading(true)
            axios
                .post('https://desa.agasyan.my.id/api/komentar-pengumuman', {
                    title: "",
                    isi: inputComment,
                    pengumuman_id: info.id,
                    user_id: getUserData().id
                })
                .then(() => {
                    setInputComment("");
                    setSendLoading(false)
                    setComments([])
                    fetchData()
                })
                .catch((error) => {
                    setInputComment("");
                    setSendLoading(false)
                    console.log(error)
                });
            event.preventDefault();
        }
    }
    return (<Card fullWidth {...rest}>
        <CardMedia
            component="img"
            height="140"
            image={info.gambar}
            alt="info image"
        />
        <CardContent>
            <Typography gutterBottom variant="h5" component="div">
                {info.title}
            </Typography>
            <Typography paragraph>
                {info.isi}
            </Typography>
            <Typography variant="overline">
                Dibuat oleh {info.created_user.full_name}
            </Typography>
        </CardContent>
        <CardActions>
            <ExpandMore
                expand={expanded}
                onClick={handleExpandClick}
                aria-expanded={expanded}
                aria-label="show comment"
            >
                <ExpandMoreIcon />
            </ExpandMore>
        </CardActions>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
            <CardContent>
                {comments.map((comment) => <CommentCard key={comment.id} comment={comment} />)}
                <FormControl fullWidth sx={{ mt: 4 }}>
                    <InputLabel htmlFor="send-comment">Tambah Komentar</InputLabel>
                    <FilledInput
                        id="send-comment"
                        onChange={(event) => { setInputComment(event.target.value) }}
                        endAdornment={
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="send icon"
                                    edge="end"
                                    type='submit'
                                    onClick={handleSendIcon}
                                >
                                    {sendLoading ? <CircularProgress /> : <SendIcon />}
                                </IconButton>
                            </InputAdornment>
                        }
                        label="Tambah Komentar"
                    />
                    {loading && <CircularProgress />}
                </FormControl>
            </CardContent>
        </Collapse>
    </Card>
    );
}
