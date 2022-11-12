import { Card, CardContent, Typography } from "@mui/material"

export const CommentCard = ({ comment, ...rest }) => {
    return (
        <Card sx={{ width: "auto" }} {...rest}>
            <CardHeader
                avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
                        {comment.author.charAt(0)}
                    </Avatar>
                }
                action={
                    <IconButton aria-label="settings">
                        <MoreVertIcon />
                    </IconButton>
                }
                title={comment.author}
                subheader={comment.created_at}
            />
            <CardContent>
                <Typography variant="body2" color="text.secondary">
                    {comment.content}
                </Typography>
            </CardContent>
        </Card >
    );
}