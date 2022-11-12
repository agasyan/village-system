import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useState } from 'react';
import { Collapse, FilledInput, FormControl, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { CommentCard } from './comment-card';

const ExpandMore = styled((props) => {
    const { expand, ...other } = props;
    return <IconButton {...other} />;
})(({ theme, expand }) => ({
    transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
    }),
}));

export const InfoCard = ({ info, ...rest }) => {

    const [expanded, setExpanded] = useState(false)

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };
    const handleSendIcon = () => {
        
    }
    return (<Card fullWidth {...rest}>
        <CardMedia
            component="img"
            height="140"
            image={info.image}
            alt="info image"
        />
        <CardContent>
            <Typography gutterBottom variant="h5" component="div">
                {info.title}
            </Typography>
            <Typography paragraph>
                {info.content}
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
                {info.comments.map((comment) => <CommentCard comment={comment} />)}
                <FormControl fullWidth sx={{ m: 1 }}>
                    <InputLabel htmlFor="send-comment">Tambah Komentar</InputLabel>
                    <FilledInput
                        id="send-comment"
                        endAdornment={
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="send icon"
                                    onClick={handleSendIcon}
                                    edge="end"
                                >
                                    <SendIcon />
                                </IconButton>
                            </InputAdornment>
                        }
                        label="Tambah Komentar"
                    />
                </FormControl>
            </CardContent>
        </Collapse>
    </Card>
    );
}
