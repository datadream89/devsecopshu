import React, { useState } from "react";
import { Box, Typography, IconButton } from "@mui/material";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const TitleBar = ({ title, expanded, toggleExpanded, checked, onCheckChange }) => (
  <Box
    display="flex"
    alignItems="center"
    bgcolor="#f5f5f5"
    px={2}
    py={1}
    borderTop={1}
    borderBottom={1}
    borderColor="grey.400"
    mb={1}
  >
    <input
      type="checkbox"
      checked={checked}
      onChange={onCheckChange}
      style={{ marginRight: 10 }}
    />
    <Typography variant="subtitle1" flex={1}>
      {title}
    </Typography>
    <IconButton onClick={toggleExpanded} size="small">
      {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
    </IconButton>
  </Box>
);

const HorizontalPair = ({ leftComponent, rightComponent, title }) => {
  const [expanded, setExpanded] = useState(true);
  const [checked, setChecked] = useState(true);

  return (
    <Box mb={4}>
      <TitleBar
        title={title}
        expanded={expanded}
        toggleExpanded={() => setExpanded(!expanded)}
        checked={checked}
        onCheckChange={(e) => setChecked(e.target.checked)}
      />
      {expanded && (
        <Box display="flex" gap={2} mt={1} px={1}>
          <Box
            flex={1}
            border={1}
            borderColor={checked ? "grey.500" : "grey.300"}
            borderRadius={2}
            bgcolor="white"
            sx={{ opacity: checked ? 1 : 0.5, transition: "opacity 0.3s ease" }}
            p={2}
          >
            {leftComponent}
          </Box>
          <Box
            flex={1}
            border={1}
            borderColor={checked ? "grey.500" : "grey.300"}
            borderRadius={2}
            bgcolor="white"
            sx={{ opacity: checked ? 1 : 0.5, transition: "opacity 0.3s ease" }}
            p={2}
          >
            {rightComponent}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default HorizontalPair;
