import React, { useState } from "react";
import { Box, Typography, IconButton, Button } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

const BidirectionalArrow = ({
  leftSelected,
  rightSelected,
  onLeftClick,
  onRightClick,
}) => (
  <Box
    display="flex"
    flexDirection="column"
    justifyContent="center"
    alignItems="center"
    mx={1}
  >
    <IconButton
      size="small"
      onClick={onLeftClick}
      sx={{ color: leftSelected ? "grey.800" : "grey.400" }}
      aria-label="Highlight left box"
    >
      <ArrowBackIcon />
    </IconButton>
    <IconButton
      size="small"
      onClick={onRightClick}
      sx={{ color: rightSelected ? "grey.800" : "grey.400" }}
      aria-label="Highlight right box"
    >
      <ArrowForwardIcon />
    </IconButton>
  </Box>
);

const TitleBar = ({ title, expanded, toggleExpanded }) => (
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
    sx={{ userSelect: "none" }}
  >
    <Typography
      variant="subtitle1"
      flex={1}
      sx={{ userSelect: "none", fontWeight: 600 }}
    >
      {title}
    </Typography>
    <IconButton
      onClick={toggleExpanded}
      aria-label={expanded ? "Collapse section" : "Expand section"}
      size="small"
    >
      {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
    </IconButton>
  </Box>
);

const PSCRFSection = () => (
  <Box p={2}>
    <Typography>PSCRF Content here...</Typography>
  </Box>
);

const ContractSection = ({ title }) => (
  <Box p={2}>
    <Typography>{title} content here...</Typography>
  </Box>
);

const BoxPair = ({ leftComponent, rightComponent, title, visible }) => {
  const [expanded, setExpanded] = useState(true);
  const [leftArrowSelected, setLeftArrowSelected] = useState(false);
  const [rightArrowSelected, setRightArrowSelected] = useState(false);

  if (!visible) return null;

  const toggleExpanded = () => setExpanded((v) => !v);
  const toggleLeftArrow = () => setLeftArrowSelected((v) => !v);
  const toggleRightArrow = () => setRightArrowSelected((v) => !v);

  const leftBoxStyle = {
    opacity: 1,
    borderColor: leftArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };
  const rightBoxStyle = {
    opacity: 1,
    borderColor: rightArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };

  return (
    <Box mb={3}>
      <TitleBar title={title} expanded={expanded} toggleExpanded={toggleExpanded} />
      {expanded && (
        <Box display="flex" alignItems="center" gap={1}>
          <Box
            flex={1}
            border={1}
            borderRadius={2}
            sx={leftBoxStyle}
            minHeight={250}
            bgcolor="white"
          >
            {leftComponent}
          </Box>
          <BidirectionalArrow
            leftSelected={leftArrowSelected}
            rightSelected={rightArrowSelected}
            onLeftClick={toggleLeftArrow}
            onRightClick={toggleRightArrow}
          />
          <Box
            flex={1}
            border={1}
            borderRadius={2}
            sx={rightBoxStyle}
            minHeight={250}
            bgcolor="white"
          >
            {rightComponent}
          </Box>
        </Box>
      )}
    </Box>
  );
};

const ComparisonLayout = () => {
  const [visibleRows, setVisibleRows] = useState([true, true, true, true]);

  const toggleRowVisibility = (index) => {
    setVisibleRows((prev) => prev.map((v, i) => (i === index ? !v : v)));
  };

  const rowTitles = ["Row 1", "Row 2", "Row 3", "Row 4"];

  return (
    <Box
      sx={{
        width: "95vw",
        maxWidth: 1200,
        mx: "auto",
        mt: 3,
        mb: 6,
        px: 1,
        userSelect: "none",
      }}
    >
      {/* Buttons to toggle row visibility */}
      <Box mb={2} display="flex" gap={2}>
        {rowTitles.map((title, i) => (
          <Button
            key={title}
            variant={visibleRows[i] ? "contained" : "outlined"}
            onClick={() => toggleRowVisibility(i)}
          >
            {title}
          </Button>
        ))}
      </Box>

      {/* Rows rendered conditionally */}
      {visibleRows[0] && (
        <BoxPair
          title="Row 1"
          visible={visibleRows[0]}
          leftComponent={<PSCRFSection />}
          rightComponent={<ContractSection title="Approved Contract" />}
        />
      )}
      {visibleRows[1] && (
        <BoxPair
          title="Row 2"
          visible={visibleRows[1]}
          leftComponent={<ContractSection title="Approved Contract" />}
          rightComponent={<ContractSection title="Signed Contract" />}
        />
      )}
      {visibleRows[2] && (
        <BoxPair
          title="Row 3"
          visible={visibleRows[2]}
          leftComponent={<ContractSection title="Signed Contract" />}
          rightComponent={<PSCRFSection />}
        />
      )}
      {visibleRows[3] && (
        <BoxPair
          title="Row 4"
          visible={visibleRows[3]}
          leftComponent={<PSCRFSection />}
          rightComponent={<PSCRFSection />}
        />
      )}
    </Box>
  );
};

export default ComparisonLayout;
